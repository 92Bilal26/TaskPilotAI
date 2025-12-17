"""ChatKit API Endpoints

Implements OpenAI ChatKit SDK backend specification.
Handles threads, messages, and assistant runs for ChatKit integration.
"""

import logging
import json
from typing import Optional, Dict, Any
from fastapi import APIRouter, HTTPException, Depends, Request
from pydantic import BaseModel, Field
from sqlmodel import Session
from openai import OpenAI
from config import settings
from db import get_session

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/api/v1/chatkit", tags=["chatkit"])

# Initialize OpenAI client for ChatKit
client = OpenAI(api_key=settings.OPENAI_API_KEY)

# ChatKit Assistant ID - Generated via setup_chatkit_assistant.py
# This is the OpenAI Assistant configured to handle ChatKit conversations
CHATKIT_ASSISTANT_ID = "asst_jpz7GaRb0d6qXdUUjIaoZ4xq"


class ThreadRequest(BaseModel):
    """Request to create a new thread"""
    metadata: Optional[Dict[str, Any]] = None


class MessageRequest(BaseModel):
    """Request to add a message to a thread"""
    content: str = Field(..., min_length=1, max_length=5000)
    metadata: Optional[Dict[str, Any]] = None


class ThreadResponse(BaseModel):
    """ChatKit thread response"""
    id: str
    created_at: int
    metadata: Optional[Dict[str, Any]] = None


class MessageResponse(BaseModel):
    """ChatKit message response"""
    id: str
    thread_id: str
    role: str
    content: str
    created_at: int
    metadata: Optional[Dict[str, Any]] = None


async def get_user_id_from_request(request: Request) -> str:
    """Extract user_id from JWT token in request"""
    user_id = getattr(request.state, "user_id", None)
    if not user_id:
        raise HTTPException(status_code=401, detail="User not authenticated")
    return user_id


@router.post("/threads", response_model=ThreadResponse)
async def create_thread(
    thread_req: ThreadRequest,
    request: Request,
    user_id: str = Depends(get_user_id_from_request),
) -> ThreadResponse:
    """
    Create a new ChatKit thread.

    Args:
        thread_req: Thread creation request
        request: HTTP request
        user_id: User ID from JWT token

    Returns:
        ThreadResponse with thread ID
    """
    logger.info(f"Creating ChatKit thread for user {user_id}")

    try:
        # Add user_id to metadata
        metadata = thread_req.metadata or {}
        metadata["user_id"] = user_id

        # Create thread with OpenAI SDK
        thread = client.beta.threads.create(metadata=metadata)

        logger.info(f"Created thread {thread.id} for user {user_id}")

        return ThreadResponse(
            id=thread.id,
            created_at=int(thread.created_at),
            metadata=thread.metadata,
        )

    except Exception as e:
        logger.error(f"Error creating thread: {e}")
        raise HTTPException(status_code=500, detail=f"Error creating thread: {str(e)}")


@router.get("/threads/{thread_id}", response_model=ThreadResponse)
async def get_thread(
    thread_id: str,
    request: Request,
    user_id: str = Depends(get_user_id_from_request),
) -> ThreadResponse:
    """
    Get a specific thread.

    Args:
        thread_id: Thread ID
        request: HTTP request
        user_id: User ID from JWT token

    Returns:
        ThreadResponse with thread details
    """
    logger.info(f"Retrieving thread {thread_id} for user {user_id}")

    try:
        thread = client.beta.threads.retrieve(thread_id)

        # Verify user owns this thread
        if thread.metadata.get("user_id") != user_id:
            raise HTTPException(status_code=403, detail="Not authorized to access this thread")

        logger.info(f"Retrieved thread {thread_id}")

        return ThreadResponse(
            id=thread.id,
            created_at=int(thread.created_at),
            metadata=thread.metadata,
        )

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error retrieving thread: {e}")
        raise HTTPException(status_code=500, detail=f"Error retrieving thread: {str(e)}")


@router.post("/threads/{thread_id}/messages", response_model=MessageResponse)
async def create_message(
    thread_id: str,
    message_req: MessageRequest,
    request: Request,
    user_id: str = Depends(get_user_id_from_request),
) -> MessageResponse:
    """
    Add a message to a thread.

    Args:
        thread_id: Thread ID
        message_req: Message creation request
        request: HTTP request
        user_id: User ID from JWT token

    Returns:
        MessageResponse with message details
    """
    logger.info(f"Adding message to thread {thread_id} for user {user_id}")

    try:
        # Verify user owns this thread
        thread = client.beta.threads.retrieve(thread_id)
        if thread.metadata.get("user_id") != user_id:
            raise HTTPException(status_code=403, detail="Not authorized to access this thread")

        # Add metadata
        metadata = message_req.metadata or {}
        metadata["user_id"] = user_id

        # Create message
        message = client.beta.threads.messages.create(
            thread_id=thread_id,
            role="user",
            content=message_req.content,
            metadata=metadata,
        )

        # Run assistant
        logger.info(f"Running assistant for thread {thread_id}")
        run = client.beta.threads.runs.create(
            thread_id=thread_id,
            assistant_id=CHATKIT_ASSISTANT_ID,
        )

        # Wait for run to complete (with timeout)
        max_attempts = 30
        attempts = 0
        while attempts < max_attempts:
            run_status = client.beta.threads.runs.retrieve(thread_id, run.id)
            if run_status.status == "completed":
                break
            elif run_status.status == "failed":
                raise Exception(f"Assistant run failed: {run_status.last_error}")
            attempts += 1
            import time
            time.sleep(0.2)

        logger.info(f"Assistant run completed for thread {thread_id}")

        return MessageResponse(
            id=message.id,
            thread_id=thread_id,
            role="user",
            content=message_req.content,
            created_at=int(message.created_at),
            metadata=message.metadata,
        )

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error creating message: {e}")
        raise HTTPException(status_code=500, detail=f"Error creating message: {str(e)}")


@router.get("/threads/{thread_id}/messages")
async def get_thread_messages(
    thread_id: str,
    limit: int = 10,
    request: Request = None,
    user_id: str = Depends(get_user_id_from_request),
) -> Dict[str, Any]:
    """
    Get all messages in a thread.

    Args:
        thread_id: Thread ID
        limit: Maximum number of messages to retrieve
        request: HTTP request
        user_id: User ID from JWT token

    Returns:
        Dictionary with messages list
    """
    logger.info(f"Retrieving messages for thread {thread_id} (limit={limit})")

    try:
        # Verify user owns this thread
        thread = client.beta.threads.retrieve(thread_id)
        if thread.metadata.get("user_id") != user_id:
            raise HTTPException(status_code=403, detail="Not authorized to access this thread")

        # Get messages
        messages = client.beta.threads.messages.list(thread_id, limit=limit)

        # Format response
        formatted_messages = []
        for msg in messages.data:
            # Extract text content
            content_text = ""
            if hasattr(msg, "content") and len(msg.content) > 0:
                content_obj = msg.content[0]
                if hasattr(content_obj, "text"):
                    content_text = content_obj.text.value

            formatted_messages.append({
                "id": msg.id,
                "thread_id": thread_id,
                "role": msg.role,
                "content": content_text,
                "created_at": int(msg.created_at),
                "metadata": msg.metadata,
            })

        logger.info(f"Retrieved {len(formatted_messages)} messages from thread {thread_id}")

        return {
            "thread_id": thread_id,
            "messages": formatted_messages,
            "has_more": messages.has_more if hasattr(messages, "has_more") else False,
        }

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error retrieving messages: {e}")
        raise HTTPException(status_code=500, detail=f"Error retrieving messages: {str(e)}")


@router.get("/health")
async def health_check():
    """Health check endpoint for ChatKit"""
    return {"status": "ok", "service": "chatkit"}
