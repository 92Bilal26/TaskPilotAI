"""ChatKit Python SDK Server Wrapper

This module implements the ChatKit Python SDK ChatKitServer interface to bridge
ChatKit frontend with the existing custom chatbot backend (Agents SDK + MCP tools).

Architecture:
    ChatKit UI → ChatKit Protocol → MyChatKitServer → Agents SDK → MCP Tools → Database
"""

from typing import AsyncIterator, Optional, Dict, Any
from datetime import datetime, timedelta
import logging
import uuid
import httpx
import json
import base64

from fastapi import APIRouter, HTTPException, Request, Depends
from fastapi.responses import StreamingResponse, Response, JSONResponse
from pydantic import BaseModel
from openai import OpenAI
from jose import jwt as jose_jwt
from chatkit.server import ChatKitServer
from chatkit.store import Store
from chatkit.types import (
    UserMessageItem, ThreadMetadata,
    ErrorEvent, NoticeEvent, WidgetItem, Page
)
from chatkit.widgets import Card, ListViewItem, Text, Title
from chatkit.agents import AgentContext, simple_to_agent_input, stream_agent_response
from agents import Runner

from sqlmodel import Session, select
from db import get_session
from models import Conversation, Message, ChatKitSession
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

    async def load_thread_items(
        self,
        thread_id: str,
        after: str | None,
        limit: int,
        order: str,
        context,
    ):
        """Load thread items with pagination - returns Page object"""
        items = self.items.get(thread_id, [])

        # Sort by creation time
        items.sort(key=lambda i: i.created_at, reverse=(order == "desc"))

        # Filter by 'after' cursor if provided
        if after:
            after_index = next((i for i, item in enumerate(items) if item.id == after), -1)
            if after_index >= 0:
                items = items[after_index + 1:]

        # Apply pagination
        has_more = len(items) > limit
        items = items[:limit]

        # Return Page object with proper structure (uses 'data' field, not 'items')
        return Page(
            data=items,
            has_more=has_more,
            after=items[-1].id if items else None
        )

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

    async def load_threads(self, context, limit: int = 10, after: str = None, order: str = "desc", **kwargs):
        """Load threads with pagination - returns Page object with has_more attribute"""
        threads = list(self.threads.values())

        # Sort by creation time
        threads.sort(key=lambda t: t.created_at, reverse=(order == "desc"))

        # Filter by 'after' cursor if provided
        if after:
            after_index = next((i for i, t in enumerate(threads) if t.id == after), -1)
            if after_index >= 0:
                threads = threads[after_index + 1:]

        # Apply pagination
        has_more = len(threads) > limit
        items = threads[:limit]

        # Return Page object with proper structure (uses 'data' field, not 'items')
        return Page(
            data=items,
            has_more=has_more,
            # Include the last thread's ID as cursor for next page
            after=items[-1].id if items else None
        )

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
        """Process user message and stream AI response using official ChatKit agents pattern.

        Uses the official ChatKit agents library pattern:
        - Runner.run_streamed() for streaming agent execution
        - stream_agent_response() for proper event yielding
        - simple_to_agent_input() for message conversion

        Args:
            thread: ChatKit thread metadata
            input: User message item
            context: Request context with user_id

        Yields:
            ThreadStreamEvent (NoticeEvent, ErrorEvent, etc.)
        """
        try:
            # Extract user_id for user isolation (T023)
            user_id = getattr(context, 'user_id', None) or context.headers.get("X-User-ID")
            if not user_id:
                yield ErrorEvent(level='danger', message="Authentication required")
                return

            logger.info(f"ChatKit respond: user={user_id}, thread={thread.id}")

            # Add the current user message to the thread first
            await self.store.add_thread_item(thread.id, input, context)
            logger.info(f"Added user message to thread: {input.id if hasattr(input, 'id') else 'unknown'}")

            # Load thread items and convert to agent input
            items_page = await self.store.load_thread_items(
                thread.id,
                after=None,
                limit=30,
                order="desc",
                context=context,
            )
            items = list(reversed(items_page.data))
            agent_input = await simple_to_agent_input(items)

            logger.info(f"Loaded {len(items)} thread items for agent (including user message)")

            # Initialize MCP tools for agent and wrap them to inject user_id
            mcp_server = initialize_mcp_server()
            raw_tools = mcp_server.get_tools()

            # Create wrapper functions that inject user_id into tool calls
            # This ensures user isolation when tools are called by the agent
            wrapped_tools = []

            # Import the original tool functions to wrap them
            from mcp.tools import add_task as mcp_add_task
            from mcp.tools import list_tasks as mcp_list_tasks
            from mcp.tools import delete_task as mcp_delete_task
            from mcp.tools import complete_task as mcp_complete_task
            from mcp.tools import update_task as mcp_update_task
            from mcp.tools import find_task_by_name as mcp_find_task_by_name

            # Create wrapper for add_task that automatically includes user_id
            def add_task_wrapper(title: str, description: str = None):
                """Add a task with automatic user isolation"""
                logger.info(f"add_task called for user {user_id}")
                return mcp_add_task(user_id=user_id, title=title, description=description)

            # Create wrapper for list_tasks that automatically includes user_id
            def list_tasks_wrapper(status: str = "all"):
                """List tasks with automatic user isolation"""
                logger.info(f"list_tasks called for user {user_id}")
                return mcp_list_tasks(user_id=user_id, status=status)

            # Create wrapper for delete_task that automatically includes user_id
            def delete_task_wrapper(task_id: str):
                """Delete a task with automatic user isolation"""
                logger.info(f"delete_task called for user {user_id}")
                return mcp_delete_task(user_id=user_id, task_id=task_id)

            # Create wrapper for complete_task that automatically includes user_id
            def complete_task_wrapper(task_id: str):
                """Mark a task as complete with automatic user isolation"""
                logger.info(f"complete_task called for user {user_id}")
                return mcp_complete_task(user_id=user_id, task_id=task_id)

            # Create wrapper for update_task that automatically includes user_id
            def update_task_wrapper(task_id: str, title: str = None, description: str = None):
                """Update a task with automatic user isolation"""
                logger.info(f"update_task called for user {user_id}")
                return mcp_update_task(user_id=user_id, task_id=task_id, title=title, description=description)

            # Create wrapper for find_task_by_name that automatically includes user_id
            def find_task_by_name_wrapper(name: str):
                """Find a task by name with automatic user isolation"""
                logger.info(f"find_task_by_name called for user {user_id}")
                return mcp_find_task_by_name(user_id=user_id, name=name)

            # Use wrapped tools instead of raw tools
            wrapped_tools = [
                add_task_wrapper,
                list_tasks_wrapper,
                delete_task_wrapper,
                complete_task_wrapper,
                update_task_wrapper,
                find_task_by_name_wrapper,
            ]

            logger.info(f"Initialized MCP with {len(wrapped_tools)} wrapped tools")

            # Create agent with wrapped tools that include user_id
            try:
                task_agent = create_task_agent(tools=wrapped_tools)
            except ValueError as e:
                logger.error(f"Agent init failed: {e}")
                yield ErrorEvent(level='danger', message="Agent initialization failed")
                return

            # Create agent context for streaming
            agent_context = AgentContext(
                thread=thread,
                store=self.store,
                request_context=context,
            )

            # Stream agent response using official pattern
            # Note: task_agent is a TaskManagementAgent wrapper, need to pass task_agent.agent
            logger.info("Starting agent streaming...")
            result = Runner.run_streamed(
                task_agent.agent,  # Pass the underlying Agent object, not the wrapper
                agent_input,
                context=agent_context,  # Include context parameter
            )

            # Yield events as they stream in
            async for event in stream_agent_response(agent_context, result):
                yield event
                logger.debug(f"Yielded event: {type(event).__name__}")

        except Exception as e:
            logger.error(f"Error in respond: {str(e)}", exc_info=True)
            yield ErrorEvent(
                level='danger',
                message=f"Error: {str(e)}"
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

    def _verify_user_conversation_access(
        self,
        session: Session,
        conversation_id: int,
        user_id: str
    ) -> Conversation:
        """Verify that user has access to conversation (User Isolation - T023).

        T023: Implement user isolation middleware
        - Validate that the conversation belongs to the requesting user
        - Prevent users from accessing other users' conversations

        Args:
            session: Database session
            conversation_id: Conversation ID to verify access for
            user_id: User ID from JWT token

        Returns:
            Conversation object if user has access

        Raises:
            HTTPException: 404 if conversation not found, 403 if not authorized
        """
        stmt = select(Conversation).where(Conversation.id == conversation_id)
        conversation = session.exec(stmt).first()

        if not conversation:
            logger.warning(f"Conversation {conversation_id} not found")
            raise HTTPException(status_code=404, detail="Conversation not found")

        # T023: Check user isolation - user can only access their own conversations
        if conversation.user_id != user_id:
            logger.warning(
                f"Unauthorized access: user {user_id} tried to access "
                f"conversation {conversation_id} owned by {conversation.user_id}"
            )
            raise HTTPException(
                status_code=403,
                detail="Unauthorized: conversation belongs to different user"
            )

        logger.debug(f"User {user_id} verified access to conversation {conversation_id}")
        return conversation

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

    def _create_task_list_widget(self, tool_call: Dict[str, Any]) -> Optional[Any]:
        """Create a ChatKit Card widget displaying list of tasks.

        Converts tool_call result (task list JSON) into a Card widget with ListView
        showing task details (id, title, completed status).

        Args:
            tool_call: Tool execution record with result containing task list JSON

        Returns:
            WidgetItem with Card/ListView widget, or None if parsing fails
        """
        try:
            result = tool_call.get("result", "")

            # Parse result string to extract task list
            # Result format: "Task 1: title\nTask 2: title" or JSON
            tasks = []
            if isinstance(result, str):
                # Handle JSON format if result is JSON
                try:
                    if result.startswith("["):
                        import json as json_module
                        tasks = json_module.loads(result)
                    else:
                        # Parse text format: each line is a task
                        lines = result.strip().split("\n")
                        for line in lines:
                            if line.strip():
                                # Simple parsing: "Task X: title" or "- title (completed/pending)"
                                if ": " in line:
                                    parts = line.split(": ", 1)
                                    title = parts[1]
                                else:
                                    title = line.strip()

                                # Extract completion status
                                completed = "✓" in line or "(completed)" in line.lower()
                                tasks.append({
                                    "title": title,
                                    "completed": completed
                                })
                except Exception:
                    # If parsing fails, return None to fall back to text format
                    logger.warning(f"Failed to parse task list result: {result}")
                    return None

            # Handle case where result is already a list of dicts
            elif isinstance(result, list):
                tasks = result

            # If no tasks, show empty state
            if not tasks:
                return None  # Will use fallback text message

            # Create Card with title and task items directly
            card_children = [
                Title(
                    type="Title",
                    value=f"📋 Your Tasks ({len(tasks)})",
                    size="md"
                )
            ]

            # Add task items directly to card (max 10)
            for i, task in enumerate(tasks):
                if i >= 10:  # Limit to 10 tasks
                    break

                if isinstance(task, dict):
                    task_title = task.get("title", task.get("name", f"Task {i+1}"))
                    is_completed = task.get("completed", False)
                else:
                    task_title = str(task)
                    is_completed = False

                # Create visual indicator for completion status
                status_icon = "✓" if is_completed else "○"
                item_text = f"{status_icon} {task_title}"

                list_item = ListViewItem(
                    type="ListViewItem",
                    children=[
                        Text(
                            type="Text",
                            value=item_text,
                            weight="semibold" if is_completed else "normal",
                            color="gray" if is_completed else "inherit"
                        )
                    ]
                )
                card_children.append(list_item)

            # Create Card with title and task items
            card = Card(
                type="Card",
                children=card_children,
                padding="md",
                size="full"
            )

            # Create WidgetItem to yield to ChatKit
            widget_item = WidgetItem(
                id=str(uuid.uuid4()),
                thread_id=getattr(self, '_current_thread_id', str(uuid.uuid4())),
                type='widget',
                widget=card,
                created_at=datetime.utcnow()
            )

            logger.info(f"Created task list widget with {len(tasks)} tasks")
            return widget_item

        except Exception as e:
            logger.error(f"Failed to create task list widget: {e}", exc_info=True)
            return None  # Fall back to text format

    def _format_tool_result(self, tool_call: Dict[str, Any]) -> str:
        """Format tool result for display in ChatKit UI.

        Implements hybrid approach:
        - Simple operations (add/delete/update/complete) → text confirmation with emoji
        - Find operations (find_task_by_name) → search result text
        - Complex operations (list_tasks) → handled separately with widget
          (see _create_task_list_widget)

        Args:
            tool_call: Tool execution record with keys: tool, result, status

        Returns:
            Formatted result string for display
        """
        tool_name = tool_call.get("tool", "unknown")
        result = tool_call.get("result", "")
        status = tool_call.get("status", "unknown")
        error = tool_call.get("error")

        # Handle errors first
        if error or status == "failed":
            error_msg = error or result or "Operation failed"
            return f"❌ Error: {error_msg}"

        # Simple operations → text confirmations
        if tool_name in ["add_task", "delete_task", "update_task", "complete_task"]:
            if status == "executed":
                return f"✓ {result}"
            else:
                return f"⚠️ {result}"

        # Find operations → search results
        if tool_name == "find_task_by_name":
            if result:
                return f"🔍 Found: {result}"
            else:
                return "🔍 No tasks found matching search"

        # List operations → handled separately (see _create_task_list_widget)
        if tool_name == "list_tasks":
            return "📋 Tasks list ready"

        # Default: text format
        return str(result) if result else f"✓ {tool_name} completed"


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
    db_session: Session = Depends(get_session)
) -> ChatKitSessionResponse:
    """Create a ChatKit session using OpenAI SDK.

    According to OpenAI ChatKit documentation, proper session creation requires:
    1. Using the official OpenAI SDK to create a session
    2. OpenAI SDK returns a properly formatted client_secret
    3. Link the session to a database conversation for persistence

    Args:
        request: FastAPI request with user context
        db_session: Database session

    Returns:
        ChatKitSessionResponse with proper client_secret from OpenAI SDK
    """
    try:
        # Extract user_id from request state (set by auth middleware)
        user_id = getattr(request.state, "user_id", None)
        if not user_id:
            user_id = request.headers.get("X-User-ID")
        if not user_id:
            raise HTTPException(status_code=401, detail="User not authenticated")

        logger.info(f"Creating ChatKit session for user: {user_id}")

        # For custom ChatKit backend (advanced integration):
        # The client_secret is just a session identifier
        # It doesn't need to be a JWT - just a unique string
        session_id = str(uuid.uuid4())

        # For custom backends, the client_secret is simply the session ID
        # The ChatKit SDK stores this and sends it back with subsequent requests
        client_secret = session_id

        logger.info(f"Generated custom ChatKit session {session_id} for user {user_id}")

        # Create conversation in our database for persistence
        conversation = Conversation(
            user_id=user_id,
            title=f"ChatKit Session {datetime.utcnow().strftime('%Y-%m-%d %H:%M')}",
            created_at=datetime.utcnow(),
            updated_at=datetime.utcnow()
        )
        db_session.add(conversation)
        db_session.commit()
        db_session.refresh(conversation)
        logger.info(f"Created database conversation {conversation.id}")

        # Create ChatKitSession record to link OpenAI session to our conversation
        expires_at = datetime.utcnow() + timedelta(
            seconds=settings.CHATKIT_SESSION_TIMEOUT
        )

        chatkit_session_record = ChatKitSession(
            session_id=session_id,  # Use the actual session ID from OpenAI
            user_id=user_id,
            conversation_id=conversation.id,
            expires_at=expires_at,
            created_at=datetime.utcnow()
        )
        db_session.add(chatkit_session_record)

        # Link conversation to ChatKit session
        conversation.chatkit_session_id = session_id
        db_session.commit()
        logger.info(f"Created ChatKit session link {session_id}")

        # Return the properly formatted client_secret from OpenAI API
        return ChatKitSessionResponse(
            client_secret=client_secret,
            session_id=session_id,
            conversation_id=conversation.id
        )

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Failed to create ChatKit session: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail="Failed to create session")


# ChatKit Protocol Endpoint (Advanced Integration)
@router.post("/chatkit")
async def chatkit_protocol_endpoint(
    request: Request,
    db_session: Session = Depends(get_session)
):
    """ChatKit server protocol endpoint for advanced integration.

    This endpoint implements the ChatKit server protocol directly.
    It handles:
    - Session initialization
    - Message processing
    - Streaming responses

    The frontend sends requests in the ChatKit protocol format
    and receives responses with conversation events.
    """
    try:
        # Extract user_id from auth middleware or headers
        user_id = getattr(request.state, "user_id", None)
        if not user_id:
            user_id = request.headers.get("X-User-ID")

        logger.info(f"ChatKit protocol request from user: {user_id}")

        # Get request body
        body = await request.body()

        # Process through ChatKit server
        # Context object includes user_id for middleware validation
        context = type('Context', (), {'user_id': user_id, 'request': request, 'db_session': db_session})()

        result = await chatkit_server.process(body, context)

        # Handle streaming vs regular responses
        from chatkit.server import StreamingResult

        if isinstance(result, StreamingResult):
            # StreamingResult is an AsyncIterable[bytes], use it directly
            return StreamingResponse(
                result,
                media_type="text/event-stream"
            )

        # Non-streaming response - check for json property (not method)
        if hasattr(result, 'json'):
            return Response(content=result.json, media_type="application/json")

        # Fallback for plain dict responses
        return JSONResponse(result)

    except Exception as e:
        logger.error(f"ChatKit protocol error: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail=str(e))
