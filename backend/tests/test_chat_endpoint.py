"""Tests for Chat API Endpoints

Tests for:
- POST /api/{user_id}/chat: Send chat message
- Conversation creation and persistence
- Message storage with tool_calls
- User isolation
"""

import pytest
from fastapi.testclient import TestClient
from sqlmodel import Session, select
from main import app
from models import Conversation, Message, User
from db import engine
from datetime import datetime


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
    """Create test user"""
    import uuid
    user = User(
        id=str(uuid.uuid4()),
        email="test@example.com",
        name="Test User",
        password_hash="hashed_password",
        emailVerified=True,
    )
    db_session.add(user)
    db_session.commit()
    db_session.refresh(user)
    return user


@pytest.fixture
def auth_header(test_user: User):
    """Create JWT auth header for test user"""
    from jose import jwt
    from config import settings

    token = jwt.encode(
        {"user_id": test_user.id},
        settings.JWT_SECRET,
        algorithm=settings.JWT_ALGORITHM,
    )
    return {"Authorization": f"Bearer {token}"}


def test_chat_endpoint_requires_auth(client: TestClient):
    """Test: Chat endpoint requires authentication"""
    # Act
    response = client.post(
        "/api/test-user/chat",
        json={"content": "Hello"},
        headers={},
    )

    # Assert
    assert response.status_code == 401


def test_chat_creates_new_conversation(
    client: TestClient,
    test_user: User,
    auth_header: dict,
    db_session: Session,
):
    """Test: Chat creates new conversation on first message"""
    # Act
    response = client.post(
        f"/api/{test_user.id}/chat",
        json={"content": "Hello chatbot"},
        headers=auth_header,
    )

    # Assert
    assert response.status_code == 200
    data = response.json()
    assert "conversation_id" in data
    assert data["conversation_id"] is not None

    # Verify conversation was created
    query = select(Conversation).where(
        Conversation.id == data["conversation_id"]
    )
    conv = db_session.exec(query).first()
    assert conv is not None
    assert conv.user_id == test_user.id


def test_chat_stores_user_message(
    client: TestClient,
    test_user: User,
    auth_header: dict,
    db_session: Session,
):
    """Test: User message is stored in database"""
    # Act
    response = client.post(
        f"/api/{test_user.id}/chat",
        json={"content": "Add a task to buy groceries"},
        headers=auth_header,
    )

    # Assert
    data = response.json()
    conversation_id = data["conversation_id"]

    # Verify user message was stored
    query = select(Message).where(
        Message.conversation_id == conversation_id
    ).where(
        Message.role == "user"
    )
    messages = db_session.exec(query).all()
    assert len(messages) >= 1
    assert messages[0].content == "Add a task to buy groceries"
    assert messages[0].user_id == test_user.id


def test_chat_stores_assistant_message(
    client: TestClient,
    test_user: User,
    auth_header: dict,
    db_session: Session,
):
    """Test: Assistant message is stored in database"""
    # Act
    response = client.post(
        f"/api/{test_user.id}/chat",
        json={"content": "Hello"},
        headers=auth_header,
    )

    # Assert
    data = response.json()
    conversation_id = data["conversation_id"]

    # Verify assistant message was stored
    query = select(Message).where(
        Message.conversation_id == conversation_id
    ).where(
        Message.role == "assistant"
    )
    messages = db_session.exec(query).all()
    assert len(messages) >= 1
    assert messages[0].user_id == test_user.id


def test_chat_response_includes_tool_calls(
    client: TestClient,
    test_user: User,
    auth_header: dict,
):
    """Test: Response includes tool_calls array"""
    # Act
    response = client.post(
        f"/api/{test_user.id}/chat",
        json={"content": "Add a task to buy groceries"},
        headers=auth_header,
    )

    # Assert
    data = response.json()
    assert "tool_calls" in data
    assert isinstance(data["tool_calls"], list)


def test_chat_response_includes_response_text(
    client: TestClient,
    test_user: User,
    auth_header: dict,
):
    """Test: Response includes assistant's response text"""
    # Act
    response = client.post(
        f"/api/{test_user.id}/chat",
        json={"content": "Hello chatbot"},
        headers=auth_header,
    )

    # Assert
    data = response.json()
    assert "response" in data
    assert isinstance(data["response"], str)


def test_chat_with_existing_conversation(
    client: TestClient,
    test_user: User,
    auth_header: dict,
    db_session: Session,
):
    """Test: Chat continues existing conversation"""
    # Arrange - Create first message
    response1 = client.post(
        f"/api/{test_user.id}/chat",
        json={"content": "First message"},
        headers=auth_header,
    )
    conv_id = response1.json()["conversation_id"]

    # Act - Send second message to same conversation
    response2 = client.post(
        f"/api/{test_user.id}/chat",
        json={
            "content": "Second message",
            "conversation_id": conv_id,
        },
        headers=auth_header,
    )

    # Assert
    assert response2.status_code == 200
    data = response2.json()
    assert data["conversation_id"] == conv_id

    # Verify both messages in conversation
    query = select(Message).where(
        Message.conversation_id == conv_id
    ).order_by(Message.created_at)
    messages = db_session.exec(query).all()
    assert len(messages) >= 2


def test_chat_user_isolation(
    client: TestClient,
    test_user: User,
    auth_header: dict,
    db_session: Session,
):
    """Test: User cannot access another user's conversation"""
    # Arrange - Create conversation for test user
    response = client.post(
        f"/api/{test_user.id}/chat",
        json={"content": "Private message"},
        headers=auth_header,
    )
    conv_id = response.json()["conversation_id"]

    # Create another test user
    import uuid
    other_user = User(
        id=str(uuid.uuid4()),
        email="other@example.com",
        name="Other User",
        password_hash="hashed_password",
        emailVerified=True,
    )
    db_session.add(other_user)
    db_session.commit()

    # Create auth header for other user
    from jose import jwt
    from config import settings
    token = jwt.encode(
        {"user_id": other_user.id},
        settings.JWT_SECRET,
        algorithm=settings.JWT_ALGORITHM,
    )
    other_auth_header = {"Authorization": f"Bearer {token}"}

    # Act - Try to access first user's conversation
    response = client.post(
        f"/api/{other_user.id}/chat",
        json={
            "content": "Trying to hijack",
            "conversation_id": conv_id,
        },
        headers=other_auth_header,
    )

    # Assert
    assert response.status_code == 403


def test_list_conversations(
    client: TestClient,
    test_user: User,
    auth_header: dict,
):
    """Test: GET /api/{user_id}/conversations lists user's conversations"""
    # Arrange - Create a conversation
    client.post(
        f"/api/{test_user.id}/chat",
        json={"content": "First conversation"},
        headers=auth_header,
    )

    # Act
    response = client.get(
        f"/api/{test_user.id}/conversations",
        headers=auth_header,
    )

    # Assert
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert len(data) >= 1
    assert "id" in data[0]
    assert "title" in data[0]


def test_get_conversation_messages(
    client: TestClient,
    test_user: User,
    auth_header: dict,
):
    """Test: GET /api/{user_id}/conversations/{id} gets messages"""
    # Arrange - Create conversation with messages
    response1 = client.post(
        f"/api/{test_user.id}/chat",
        json={"content": "First message"},
        headers=auth_header,
    )
    conv_id = response1.json()["conversation_id"]

    # Act
    response = client.get(
        f"/api/{test_user.id}/conversations/{conv_id}",
        headers=auth_header,
    )

    # Assert
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == conv_id
    assert "messages" in data
    assert isinstance(data["messages"], list)
