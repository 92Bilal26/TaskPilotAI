"""Chat API Endpoints

Handles chat messages and conversation management for the chatbot.
Includes multi-turn conversation support and context management.
"""

import logging
from typing import Optional, Dict, Any
from fastapi import APIRouter, HTTPException, Request, Depends
from pydantic import BaseModel, Field
from sqlmodel import Session, select
from datetime import datetime
from db import get_session
from models import Conversation, Message
from agents.openai_agent_sdk import OpenAIAgentSDK
from agents.conversation_context import get_conversation_context
from mcp.server import initialize_mcp_server

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/api", tags=["chat"])


class ChatMessage(BaseModel):
    """User chat message"""
    content: str = Field(..., min_length=1, max_length=5000)
    conversation_id: Optional[int] = None


class ChatResponse(BaseModel):
    """Chat API response"""
    conversation_id: int
    message_id: int
    response: str
    tool_calls: list[Dict[str, Any]] = []
    status: str


async def get_user_id(request: Request) -> str:
    """Extract user_id from request state"""
    user_id = getattr(request.state, "user_id", None)
    if not user_id:
        raise HTTPException(status_code=401, detail="User not authenticated")
    return user_id


@router.post("/{user_id}/chat", response_model=ChatResponse)
async def chat(
    user_id: str,
    message: ChatMessage,
    session: Session = Depends(get_session),
) -> ChatResponse:
    """
    Send a message to the chatbot.

    Args:
        user_id: User ID from JWT token
        message: Chat message with optional conversation_id
        session: Database session

    Returns:
        ChatResponse with conversation_id, message_id, response, and tool_calls
    """
    logger.info(f"Chat request from user {user_id}: {message.content[:50]}...")

    try:
        # Get or create conversation
        conversation_id = message.conversation_id
        if conversation_id:
            # Load existing conversation
            conversation = session.get(Conversation, conversation_id)
            if not conversation:
                raise HTTPException(status_code=404, detail="Conversation not found")
            if conversation.user_id != user_id:
                raise HTTPException(status_code=403, detail="Not authorized")
        else:
            # Create new conversation
            conversation = Conversation(
                user_id=user_id,
                title=None,  # Title will be set after first message
                archived=False,
                created_at=datetime.utcnow(),
                updated_at=datetime.utcnow(),
            )
            session.add(conversation)
            session.commit()
            session.refresh(conversation)
            logger.info(f"Created conversation {conversation.id} for user {user_id}")

        # Store user message
        user_msg = Message(
            conversation_id=conversation.id,
            user_id=user_id,
            role="user",
            content=message.content,
            created_at=datetime.utcnow(),
        )
        session.add(user_msg)
        session.commit()
        session.refresh(user_msg)
        logger.info(f"Stored user message {user_msg.id}")

        # Load conversation context
        conv_context = get_conversation_context(
            conversation_id=conversation.id,
            user_id=user_id,
        )

        # Get conversation history (excluding current message)
        conversation_history = conv_context.get_context(max_messages=10)

        logger.info(
            f"Loaded conversation context with {len(conversation_history)} previous messages"
        )

        # Initialize OpenAI Agents SDK agent
        try:
            agent = OpenAIAgentSDK()  # Uses OPENAI_API_KEY from config
        except ValueError as e:
            logger.error(f"Failed to initialize OpenAI Agents SDK: {e}")
            raise HTTPException(
                status_code=500,
                detail="Agent initialization failed. Check OpenAI API key configuration.",
            )

        # Initialize MCP server and register tools with agent
        mcp_server = initialize_mcp_server()
        for tool_name, tool_func in mcp_server.get_tools().items():
            agent.register_tool(tool_name, tool_func)

        logger.info(f"Agent initialized with {len(agent.get_available_tools())} tools")

        # Process message with agent
        try:
            agent_response = await agent.process_message(
                user_id=user_id,
                message=message.content,
                conversation_history=conversation_history,
            )

            # Add assistant response to context
            conv_context.add_message(
                role="assistant",
                content=agent_response.get("response", ""),
                tool_calls=agent_response.get("tool_calls"),
            )

        except Exception as e:
            logger.error(f"Agent processing failed: {e}")
            agent_response = {
                "response": f"I encountered an issue processing your request. Please try again.",
                "tool_calls": [],
                "status": "error",
            }

        # Store assistant message with tool calls
        assistant_msg = Message(
            conversation_id=conversation.id,
            user_id=user_id,
            role="assistant",
            content=agent_response.get("response", ""),
            tool_calls=agent_response.get("tool_calls", []),
            created_at=datetime.utcnow(),
        )
        session.add(assistant_msg)

        # Update conversation title if not set
        if not conversation.title:
            # Use first 100 chars of user message as title
            conversation.title = message.content[:100]
            conversation.updated_at = datetime.utcnow()

        session.commit()
        session.refresh(assistant_msg)
        logger.info(f"Stored assistant message {assistant_msg.id}")

        return ChatResponse(
            conversation_id=conversation.id,
            message_id=assistant_msg.id,
            response=agent_response.get("response", ""),
            tool_calls=agent_response.get("tool_calls", []),
            status=agent_response.get("status", "success"),
        )

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error processing chat: {e}")
        raise HTTPException(status_code=500, detail=f"Chat error: {str(e)}")


@router.get("/{user_id}/conversations")
async def list_conversations(
    user_id: str,
    session: Session = Depends(get_session),
) -> list[Dict[str, Any]]:
    """
    Get all conversations for a user.

    Args:
        user_id: User ID from JWT token
        session: Database session

    Returns:
        List of conversations with message counts
    """
    logger.info(f"Listing conversations for user {user_id}")

    try:
        query = select(Conversation).where(
            Conversation.user_id == user_id
        ).where(
            Conversation.archived == False
        ).order_by(Conversation.updated_at.desc())

        conversations = session.exec(query).all()

        result = []
        for conv in conversations:
            msg_query = select(Message).where(
                Message.conversation_id == conv.id
            )
            message_count = len(session.exec(msg_query).all())

            result.append({
                "id": conv.id,
                "title": conv.title or "New Conversation",
                "message_count": message_count,
                "created_at": conv.created_at.isoformat(),
                "updated_at": conv.updated_at.isoformat(),
            })

        return result

    except Exception as e:
        logger.error(f"Error listing conversations: {e}")
        raise HTTPException(status_code=500, detail=f"Error: {str(e)}")


@router.get("/{user_id}/conversations/{conversation_id}")
async def get_conversation_messages(
    user_id: str,
    conversation_id: int,
    session: Session = Depends(get_session),
) -> Dict[str, Any]:
    """
    Get all messages in a conversation.

    Args:
        user_id: User ID from JWT token
        conversation_id: Conversation ID
        session: Database session

    Returns:
        Conversation with messages
    """
    logger.info(f"Getting conversation {conversation_id} for user {user_id}")

    try:
        conversation = session.get(Conversation, conversation_id)
        if not conversation:
            raise HTTPException(status_code=404, detail="Conversation not found")
        if conversation.user_id != user_id:
            raise HTTPException(status_code=403, detail="Not authorized")

        # Get all messages
        msg_query = select(Message).where(
            Message.conversation_id == conversation_id
        ).order_by(Message.created_at)
        messages = session.exec(msg_query).all()

        return {
            "id": conversation.id,
            "title": conversation.title or "New Conversation",
            "created_at": conversation.created_at.isoformat(),
            "updated_at": conversation.updated_at.isoformat(),
            "messages": [
                {
                    "id": msg.id,
                    "role": msg.role,
                    "content": msg.content,
                    "tool_calls": msg.tool_calls,
                    "created_at": msg.created_at.isoformat(),
                }
                for msg in messages
            ],
        }

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error getting conversation: {e}")
        raise HTTPException(status_code=500, detail=f"Error: {str(e)}")
