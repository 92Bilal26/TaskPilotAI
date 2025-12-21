"""ChatKit Python SDK Server Wrapper

This module implements the ChatKit Python SDK ChatKitServer interface to bridge
ChatKit frontend with the existing custom chatbot backend (Agents SDK + MCP tools).

Architecture:
    ChatKit UI → ChatKit Protocol → MyChatKitServer → Agents SDK → MCP Tools → Database
"""

from typing import AsyncIterator, Optional, Dict, Any
from datetime import datetime, timedelta
import json
import logging
import uuid

from fastapi import APIRouter, HTTPException, Request, Depends
from pydantic import BaseModel
from chatkit.server import ChatKitServer
from chatkit.store import Store
from chatkit.types import (
    UserMessageItem, ThreadMetadata,
    ErrorEvent, NoticeEvent, ThreadItemAddedEvent
)

from sqlmodel import Session, select
from db import get_session
from models import Conversation, Message, ChatKitSession, Task, User
from config import settings
from task_agents.official_openai_agent import create_task_agent
from task_agents.conversation_context import get_conversation_context
from mcp.server import initialize_mcp_server

logger = logging.getLogger(__name__)


class CustomChatKitStore(Store):
    """Minimal in-memory store for ChatKit sessions.

    ChatKit requires a Store implementation for thread persistence.
    Since we store conversations in our own database, we use an in-memory
    store here that delegates persistence to MyChatKitServer.respond().
    """

    def __init__(self):
        """Initialize empty in-memory thread store"""
        self.threads = {}  # {thread_id: ThreadMetadata}
        self.items = {}  # {thread_id: [items]}

    async def load_thread(self, thread_id: str, context) -> ThreadMetadata:
        """Load thread metadata"""
        if thread_id in self.threads:
            return self.threads[thread_id]
        # Return new thread if not found
        return ThreadMetadata(
            id=thread_id,
            created_at=datetime.utcnow(),
            metadata={},
        )

    async def save_thread(self, thread: ThreadMetadata, context) -> None:
        """Save thread metadata"""
        self.threads[thread.id] = thread

    async def load_thread_items(self, thread_id: str, context):
        """Load thread items"""
        return self.items.get(thread_id, [])

    async def add_thread_item(self, thread_id: str, item, context) -> None:
        """Add item to thread"""
        if thread_id not in self.items:
            self.items[thread_id] = []
        self.items[thread_id].append(item)

    async def delete_thread(self, thread_id: str, context) -> None:
        """Delete thread"""
        self.threads.pop(thread_id, None)
        self.items.pop(thread_id, None)

    async def delete_thread_item(self, thread_id: str, item_id: str, context) -> None:
        """Delete thread item"""
        if thread_id in self.items:
            self.items[thread_id] = [
                item for item in self.items[thread_id]
                if getattr(item, 'id', None) != item_id
            ]

    async def load_item(self, thread_id: str, item_id: str, context):
        """Load specific thread item"""
        if thread_id in self.items:
            for item in self.items[thread_id]:
                if getattr(item, 'id', None) == item_id:
                    return item
        return None

    async def update_thread_item(self, thread_id: str, item_id: str, updates, context) -> None:
        """Update thread item"""
        if thread_id in self.items:
            for i, item in enumerate(self.items[thread_id]):
                if getattr(item, 'id', None) == item_id:
                    # Update item with new values
                    for key, value in updates.items():
                        setattr(item, key, value)

    async def load_threads(self, context):
        """Load all threads"""
        return list(self.threads.values())

    async def load_attachment(self, attachment_id: str, context):
        """Load attachment"""
        return None

    async def save_attachment(self, attachment, context) -> None:
        """Save attachment"""
        pass

    async def delete_attachment(self, attachment_id: str, context) -> None:
        """Delete attachment"""
        pass

    async def save_item(self, item, context) -> None:
        """Save item"""
        pass

    def generate_thread_id(self, context) -> str:
        """Generate new thread ID"""
        return str(uuid.uuid4())

    def generate_item_id(self, item_type: str, thread: ThreadMetadata, context) -> str:
        """Generate new item ID"""
        return str(uuid.uuid4())


class MyChatKitServer(ChatKitServer):
    """Custom ChatKit Server implementing ChatKitServer interface.

    Delegates message processing to existing Agents SDK + MCP tools,
    while handling ChatKit protocol and persistence.
    """

    def __init__(self):
        """Initialize ChatKit server with custom in-memory store."""
        store = CustomChatKitStore()
        super().__init__(store=store)

    async def respond(
        self,
        thread: ThreadMetadata,
        input: UserMessageItem,
        context
    ) -> AsyncIterator[ErrorEvent | NoticeEvent]:
        """Process user message and return AI response.

        Extracts user_id from context, fetches conversation history,
        delegates to Agents SDK for processing, returns response with
        tool confirmations in hybrid format.

        Args:
            thread: ChatKit thread metadata containing session info
            input: User message item
            context: Request context with user info

        Yields:
            ChatKit NoticeEvent with message content
        """
        try:
            # Extract user_id from context (JWT token)
            user_id = getattr(context, 'user_id', None) or context.headers.get("X-User-ID")
            if not user_id:
                yield ErrorEvent(
                    level='danger',
                    message="User authentication required"
                )
                return

            logger.info(f"Processing ChatKit message for user: {user_id}, session: {thread.session_id}")

            # Extract message content
            if isinstance(input, UserMessageItem):
                message_content = input.text
            elif isinstance(input, ClientToolCallOutputItem):
                message_content = input.output
            else:
                message_content = str(input)

            # Get database session
            session: Session = next(get_session())

            try:
                # Get or create conversation linked to ChatKit session
                conversation = self._get_or_create_conversation(
                    session, thread.session_id, user_id
                )
                logger.info(f"Using conversation {conversation.id}")

                # Store user message
                user_msg = Message(
                    conversation_id=conversation.id,
                    user_id=user_id,
                    role="user",
                    content=message_content,
                    created_at=datetime.utcnow(),
                )
                session.add(user_msg)
                session.commit()
                logger.info(f"Stored user message {user_msg.id}")

                # Load conversation context
                conv_context = get_conversation_context(
                    conversation_id=conversation.id,
                    user_id=user_id,
                )

                # Get conversation history (last 10 messages for context)
                conversation_history = conv_context.get_context(
                    max_messages=settings.CHATKIT_MAX_HISTORY
                )
                logger.info(f"Loaded {len(conversation_history)} previous messages")

                # Initialize MCP server and get tools
                mcp_server = initialize_mcp_server()
                tools_list = list(mcp_server.get_tools().values())
                logger.info(f"Initialized MCP with {len(tools_list)} tools")

                # Initialize agent with tools
                try:
                    agent = create_task_agent(tools=tools_list)
                except ValueError as e:
                    logger.error(f"Failed to initialize agent: {e}")
                    yield ErrorEvent(
                        level='danger',
                        message="Agent initialization failed. Check OpenAI API key."
                    )
                    return

                # Process message with agent
                try:
                    agent_response = await agent.process_message(
                        user_id=user_id,
                        message=message_content,
                        conversation_history=conversation_history,
                    )
                    logger.info(f"Agent response received: {len(agent_response.get('response', ''))} chars")

                except Exception as e:
                    logger.error(f"Agent processing failed: {e}")
                    agent_response = {
                        "response": "I encountered an issue processing your request. Please try again.",
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
                    conversation.title = message_content[:100]
                    conversation.updated_at = datetime.utcnow()

                session.commit()
                logger.info(f"Stored assistant message {assistant_msg.id}")

                # Yield AI response to ChatKit UI
                yield NoticeEvent(
                    level='info',
                    message=agent_response.get("response", "")
                )

                # Yield tool confirmations in hybrid format
                for tool_call in agent_response.get("tool_calls", []):
                    tool_response = self._format_tool_result(tool_call)
                    yield NoticeEvent(
                        level='info',
                        message=str(tool_response)
                    )

            finally:
                session.close()

        except Exception as e:
            logger.error(f"Error in respond: {str(e)}", exc_info=True)
            yield ErrorEvent(
                level='danger',
                message=f"Error processing message: {str(e)}"
            )

    async def action(
        self,
        thread: ThreadMetadata,
        action: str,
        sender: str,
        context
    ) -> AsyncIterator[NoticeEvent]:
        """Handle user actions in ChatKit UI (e.g., button clicks).

        Args:
            thread: ChatKit thread metadata
            action: Action identifier
            sender: Sender identifier
            context: Request context

        Yields:
            ChatKit NoticeEvent
        """
        logger.info(f"Handling action: {action}")
        yield NoticeEvent(
            level='info',
            message="Action received"
        )

    def _get_or_create_conversation(
        self,
        session: Session,
        chatkit_session_id: str,
        user_id: str
    ) -> Conversation:
        """Get existing conversation or create new one for ChatKit session.

        Args:
            session: Database session
            chatkit_session_id: ChatKit session ID
            user_id: User ID from JWT

        Returns:
            Conversation object
        """
        # Check if conversation already exists for this ChatKit session
        stmt = select(Conversation).where(
            Conversation.chatkit_session_id == chatkit_session_id,
            Conversation.user_id == user_id
        )
        result = session.execute(stmt)
        conversation = result.scalar_one_or_none()

        if conversation:
            logger.info(f"Found existing conversation {conversation.id}")
            return conversation

        # Create new conversation
        logger.info(f"Creating new conversation for ChatKit session {chatkit_session_id}")
        conversation = Conversation(
            user_id=user_id,
            title=f"ChatKit Session {datetime.utcnow().strftime('%Y-%m-%d %H:%M')}",
            chatkit_session_id=chatkit_session_id,
            created_at=datetime.utcnow(),
            updated_at=datetime.utcnow()
        )
        session.add(conversation)

        # Create ChatKitSession record
        expires_at = datetime.utcnow() + timedelta(
            seconds=settings.CHATKIT_SESSION_TIMEOUT
        )
        chatkit_session = ChatKitSession(
            session_id=chatkit_session_id,
            user_id=user_id,
            conversation_id=None,
            expires_at=expires_at,
            created_at=datetime.utcnow()
        )
        session.add(chatkit_session)
        session.commit()

        # Update conversation link
        conversation.chatkit_session_id = chatkit_session_id
        chatkit_session.conversation_id = conversation.id
        session.commit()
        session.refresh(conversation)

        return conversation

    def _format_tool_result(self, tool_call: Dict[str, Any]) -> str:
        """Format tool result for display in ChatKit UI.

        Implements hybrid approach:
        - Simple operations (add/delete/update/complete) → text confirmation
        - Complex operations (list_tasks) → text format with data

        Args:
            tool_call: Tool execution record

        Returns:
            Formatted result string
        """
        tool_name = tool_call.get("tool", "unknown")
        result = tool_call.get("result", "")
        status = tool_call.get("status", "unknown")

        # Simple operations → text confirmations
        if tool_name in ["add_task", "delete_task", "update_task", "complete_task"]:
            if status == "executed":
                return f"✓ {result}"
            else:
                return f"⚠️ {result}"

        # Complex operations → text format
        if tool_name == "list_tasks":
            return f"Tasks: {result}"

        # Default: text format
        return str(result)


# Initialize server instance
chatkit_server = MyChatKitServer()

# FastAPI Route Handler for Session Creation
router = APIRouter(prefix="/api/v1", tags=["chatkit"])


class ChatKitSessionResponse(BaseModel):
    """ChatKit session creation response"""
    client_secret: str
    session_id: str
    conversation_id: int


@router.post("/chatkit/sessions", response_model=ChatKitSessionResponse)
async def create_chatkit_session(
    request: Request,
    session: Session = Depends(get_session)
) -> ChatKitSessionResponse:
    """Create a ChatKit session linked to a database Conversation.

    Args:
        request: FastAPI request with user context
        session: Database session

    Returns:
        ChatKitSessionResponse with client_secret for frontend
    """
    try:
        # Extract user_id from request state (set by auth middleware)
        user_id = getattr(request.state, "user_id", None)
        if not user_id:
            # Fallback: check headers for user ID
            user_id = request.headers.get("X-User-ID")
        if not user_id:
            raise HTTPException(status_code=401, detail="User not authenticated")

        logger.info(f"Creating ChatKit session for user: {user_id}")

        # Create new conversation for this ChatKit session
        conversation = Conversation(
            user_id=user_id,
            title=f"ChatKit Session {datetime.utcnow().strftime('%Y-%m-%d %H:%M')}",
            created_at=datetime.utcnow(),
            updated_at=datetime.utcnow()
        )
        session.add(conversation)
        session.commit()
        session.refresh(conversation)
        logger.info(f"Created conversation {conversation.id}")

        # Create ChatKitSession record
        # Note: In production, session_id would come from actual ChatKit SDK initialization
        # For now, we generate a unique session_id
        chatkit_session_id = str(uuid.uuid4())
        expires_at = datetime.utcnow() + timedelta(
            seconds=settings.CHATKIT_SESSION_TIMEOUT
        )

        chatkit_session_record = ChatKitSession(
            session_id=chatkit_session_id,
            user_id=user_id,
            conversation_id=conversation.id,
            expires_at=expires_at,
            created_at=datetime.utcnow()
        )
        session.add(chatkit_session_record)

        # Update conversation with ChatKit session link
        conversation.chatkit_session_id = chatkit_session_id
        session.commit()
        logger.info(f"Created ChatKit session {chatkit_session_id}")

        # In production, this would be the actual client_secret from ChatKit SDK
        # For now, return a generated secret
        client_secret = str(uuid.uuid4())

        return ChatKitSessionResponse(
            client_secret=client_secret,
            session_id=chatkit_session_id,
            conversation_id=conversation.id
        )

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Failed to create ChatKit session: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail="Failed to create session")
