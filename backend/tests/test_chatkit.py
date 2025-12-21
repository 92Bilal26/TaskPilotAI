"""Test suite for ChatKit server wrapper and endpoints

Tests for custom ChatKit server integration with existing chatbot backend.
Verifies session creation, message processing, conversation persistence, and tool invocation.
"""

import pytest
from fastapi.testclient import TestClient
from sqlmodel import Session, select
from datetime import datetime, timedelta
from unittest.mock import patch, MagicMock, AsyncMock
import uuid

from main import app
from models import Conversation, Message, User, ChatKitSession
from db import engine
from config import settings
from routes.chatkit import MyChatKitServer, chatkit_server


@pytest.fixture
def client():
    """Provide test client"""
    return TestClient(app)


@pytest.fixture
def db_session():
    """Provide database session"""
    from db import Session
    session = Session(engine)
    yield session
    session.close()


@pytest.fixture
def test_user(db_session: Session):
    """Create test user with unique email"""
    user = User(
        id=str(uuid.uuid4()),
        email=f"chatkit-test-{uuid.uuid4()}@example.com",
        name="ChatKit Test User",
        password_hash="hashed_password",
        emailVerified=True,
    )
    db_session.add(user)
    db_session.commit()
    db_session.refresh(user)
    yield user
    # Cleanup after test
    db_session.delete(user)
    db_session.commit()


@pytest.fixture
def auth_header(test_user: User):
    """Create JWT auth header for test user"""
    from jose import jwt

    token = jwt.encode(
        {"user_id": test_user.id},
        settings.JWT_SECRET,
        algorithm=settings.JWT_ALGORITHM,
    )
    return {"Authorization": f"Bearer {token}"}


class TestChatKitSessionCreation:
    """Tests for ChatKit session creation endpoint"""

    def test_create_session_requires_auth(self, client: TestClient):
        """Test: Session creation requires authentication"""
        response = client.post("/api/v1/chatkit/sessions")
        assert response.status_code == 401

    def test_create_session_success(
        self,
        client: TestClient,
        test_user: User,
        auth_header: dict,
        db_session: Session,
    ):
        """Test: Successful ChatKit session creation"""
        # Act
        response = client.post(
            "/api/v1/chatkit/sessions",
            headers=auth_header,
        )

        # Assert
        assert response.status_code == 200
        data = response.json()
        assert "client_secret" in data
        assert "session_id" in data
        assert "conversation_id" in data
        assert isinstance(data["client_secret"], str)
        assert len(data["client_secret"]) > 0
        assert isinstance(data["session_id"], str)
        assert isinstance(data["conversation_id"], int)

    def test_create_session_creates_conversation(
        self,
        client: TestClient,
        test_user: User,
        auth_header: dict,
        db_session: Session,
    ):
        """Test: Session creation creates linked conversation"""
        # Act
        response = client.post(
            "/api/v1/chatkit/sessions",
            headers=auth_header,
        )
        session_data = response.json()
        conversation_id = session_data["conversation_id"]

        # Assert - Verify conversation was created
        query = select(Conversation).where(
            Conversation.id == conversation_id
        )
        conversation = db_session.exec(query).first()
        assert conversation is not None
        assert conversation.user_id == test_user.id
        assert conversation.title is not None

    def test_create_session_creates_chatkit_session_record(
        self,
        client: TestClient,
        test_user: User,
        auth_header: dict,
        db_session: Session,
    ):
        """Test: Session creation creates ChatKitSession database record"""
        # Act
        response = client.post(
            "/api/v1/chatkit/sessions",
            headers=auth_header,
        )
        session_data = response.json()
        session_id = session_data["session_id"]

        # Assert - Verify ChatKitSession record was created
        query = select(ChatKitSession).where(
            ChatKitSession.session_id == session_id
        )
        chatkit_session = db_session.exec(query).first()
        assert chatkit_session is not None
        assert chatkit_session.user_id == test_user.id
        assert chatkit_session.expires_at is not None

    def test_session_has_proper_expiration(
        self,
        client: TestClient,
        test_user: User,
        auth_header: dict,
        db_session: Session,
    ):
        """Test: ChatKit session has proper expiration timeout"""
        # Act
        response = client.post(
            "/api/v1/chatkit/sessions",
            headers=auth_header,
        )
        session_data = response.json()
        session_id = session_data["session_id"]

        # Assert
        query = select(ChatKitSession).where(
            ChatKitSession.session_id == session_id
        )
        chatkit_session = db_session.exec(query).first()

        # Expiration should be close to current time + timeout
        time_until_expiry = chatkit_session.expires_at - datetime.utcnow()
        timeout_seconds = settings.CHATKIT_SESSION_TIMEOUT

        # Allow 60 second buffer for test execution
        assert abs(time_until_expiry.total_seconds() - timeout_seconds) < 60

    def test_multiple_sessions_per_user(
        self,
        client: TestClient,
        test_user: User,
        auth_header: dict,
        db_session: Session,
    ):
        """Test: User can create multiple independent sessions"""
        # Act - Create two sessions
        response1 = client.post(
            "/api/v1/chatkit/sessions",
            headers=auth_header,
        )
        response2 = client.post(
            "/api/v1/chatkit/sessions",
            headers=auth_header,
        )

        # Assert - Sessions should have different IDs but same user
        data1 = response1.json()
        data2 = response2.json()

        assert data1["session_id"] != data2["session_id"]
        assert data1["conversation_id"] != data2["conversation_id"]

        # Both conversations should belong to the same user
        query = select(Conversation).where(
            Conversation.user_id == test_user.id
        )
        conversations = db_session.exec(query).all()
        assert len(conversations) >= 2


class TestChatKitServerRespond:
    """Tests for ChatKitServer.respond() method"""

    @pytest.mark.asyncio
    async def test_respond_requires_user_id(self):
        """Test: respond() requires valid user_id extraction"""
        # Arrange
        mock_thread = MagicMock()
        mock_thread.session_id = str(uuid.uuid4())

        mock_input = MagicMock()
        mock_input.text = "Hello"

        mock_context = MagicMock()
        mock_context.user_id = None
        mock_context.headers = {}

        server = MyChatKitServer()

        # Act
        events = []
        async for event in server.respond(mock_thread, mock_input, mock_context):
            events.append(event)

        # Assert - Should return error event
        assert len(events) > 0
        assert "authentication required" in events[0].text.lower() or "error" in events[0].text.lower()

    @pytest.mark.asyncio
    async def test_respond_stores_messages(self):
        """Test: respond() stores user and assistant messages"""
        # This test would require more complex setup with actual database
        # Marked as integration test placeholder
        pass

    @pytest.mark.asyncio
    async def test_respond_calls_agent(self):
        """Test: respond() delegates to Agents SDK"""
        # This test would require mocking the agent processing
        # Marked as integration test placeholder
        pass


class TestChatKitServerToolFormatting:
    """Tests for tool result formatting and widget generation"""

    def test_format_add_task_success(self):
        """Test: add_task returns checkmark confirmation"""
        server = MyChatKitServer()

        tool_call = {
            "tool": "add_task",
            "result": "Buy groceries",
            "status": "executed",
        }

        result = server._format_tool_result(tool_call)
        assert "✓" in result
        assert "Buy groceries" in result

    def test_format_delete_task_success(self):
        """Test: delete_task returns checkmark confirmation"""
        server = MyChatKitServer()

        tool_call = {
            "tool": "delete_task",
            "result": "Task deleted",
            "status": "executed",
        }

        result = server._format_tool_result(tool_call)
        assert "✓" in result

    def test_format_update_task_success(self):
        """Test: update_task returns checkmark confirmation"""
        server = MyChatKitServer()

        tool_call = {
            "tool": "update_task",
            "result": "Task updated",
            "status": "executed",
        }

        result = server._format_tool_result(tool_call)
        assert "✓" in result

    def test_format_complete_task_success(self):
        """Test: complete_task returns checkmark confirmation"""
        server = MyChatKitServer()

        tool_call = {
            "tool": "complete_task",
            "result": "Task marked complete",
            "status": "executed",
        }

        result = server._format_tool_result(tool_call)
        assert "✓" in result

    def test_format_find_task_success(self):
        """Test: find_task_by_name returns search result"""
        server = MyChatKitServer()

        tool_call = {
            "tool": "find_task_by_name",
            "result": "Buy groceries",
            "status": "executed",
        }

        result = server._format_tool_result(tool_call)
        assert "🔍" in result
        assert "Found" in result or "found" in result

    def test_format_find_task_not_found(self):
        """Test: find_task_by_name returns no results message"""
        server = MyChatKitServer()

        tool_call = {
            "tool": "find_task_by_name",
            "result": "",
            "status": "executed",
        }

        result = server._format_tool_result(tool_call)
        assert "🔍" in result
        assert "not found" in result.lower() or "No tasks" in result

    def test_format_list_tasks(self):
        """Test: list_tasks returns task list message"""
        server = MyChatKitServer()

        tool_call = {
            "tool": "list_tasks",
            "result": "Task 1: Buy groceries\nTask 2: Call mom",
            "status": "executed",
        }

        result = server._format_tool_result(tool_call)
        assert "📋" in result or "Tasks" in result

    def test_format_operation_error(self):
        """Test: Failed operations return error symbol"""
        server = MyChatKitServer()

        tool_call = {
            "tool": "add_task",
            "result": "Failed to create task",
            "status": "failed",
        }

        result = server._format_tool_result(tool_call)
        assert "❌" in result or "Error" in result

    def test_format_operation_with_error_field(self):
        """Test: Tool with error field returns error message"""
        server = MyChatKitServer()

        tool_call = {
            "tool": "delete_task",
            "result": "",
            "error": "Task not found",
            "status": "executed",
        }

        result = server._format_tool_result(tool_call)
        assert "❌" in result
        assert "Error" in result

    def test_create_task_list_widget(self):
        """Test: Widget generation for list_tasks"""
        server = MyChatKitServer()

        tool_call = {
            "tool": "list_tasks",
            "result": "✓ Buy groceries\n○ Call mom",
            "status": "executed",
        }

        widget = server._create_task_list_widget(tool_call)
        assert widget is not None
        assert hasattr(widget, 'widget')
        assert widget.type == 'widget'

    def test_create_task_list_widget_empty(self):
        """Test: Widget generation with empty task list"""
        server = MyChatKitServer()

        tool_call = {
            "tool": "list_tasks",
            "result": "",
            "status": "executed",
        }

        widget = server._create_task_list_widget(tool_call)
        assert widget is None  # Should fall back to text

    def test_format_unknown_tool(self):
        """Test: Unknown tools return default message"""
        server = MyChatKitServer()

        tool_call = {
            "tool": "unknown_operation",
            "result": "Some result",
            "status": "executed",
        }

        result = server._format_tool_result(tool_call)
        assert isinstance(result, str)
        assert len(result) > 0


class TestChatKitUserIsolation:
    """Tests for user isolation in ChatKit sessions"""

    def test_session_isolated_per_user(
        self,
        client: TestClient,
        db_session: Session,
    ):
        """Test: Users cannot access each other's ChatKit sessions"""
        # Arrange - Create two users
        user1 = User(
            id=str(uuid.uuid4()),
            email="user1@example.com",
            name="User 1",
            password_hash="hash1",
            emailVerified=True,
        )
        user2 = User(
            id=str(uuid.uuid4()),
            email="user2@example.com",
            name="User 2",
            password_hash="hash2",
            emailVerified=True,
        )
        db_session.add(user1)
        db_session.add(user2)
        db_session.commit()

        from jose import jwt

        # Create sessions for both users
        token1 = jwt.encode(
            {"user_id": user1.id},
            settings.JWT_SECRET,
            algorithm=settings.JWT_ALGORITHM,
        )
        header1 = {"Authorization": f"Bearer {token1}"}

        response1 = client.post("/api/v1/chatkit/sessions", headers=header1)
        session1_data = response1.json()
        session1_id = session1_data["session_id"]

        # Act - User2 tries to access User1's session data
        # Since ChatKit sessions are opaque to the API, user2 cannot directly access it
        # But verify that conversations are isolated at database level

        # Assert - session1 should belong to user1 only
        query = select(ChatKitSession).where(
            ChatKitSession.session_id == session1_id
        )
        session = db_session.exec(query).first()
        assert session.user_id == user1.id
        assert session.user_id != user2.id
