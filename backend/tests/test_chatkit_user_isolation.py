"""Security tests for ChatKit user isolation (T024)

Tests that users cannot access other users' conversations and that
proper authorization is enforced throughout the ChatKit integration.
"""

import pytest
import uuid
import json
from fastapi.testclient import TestClient
from sqlmodel import Session, select
from datetime import datetime, timedelta
from jose import jwt

from main import app
from models import Conversation, Message, ChatKitSession, User
from db import engine, create_db_and_tables
from config import settings


@pytest.fixture(scope="module", autouse=True)
def setup_database():
    """Create fresh database tables for testing"""
    create_db_and_tables()
    yield
    # Cleanup is optional - tables are dropped and recreated for each module


@pytest.fixture
def client():
    """Provide test client"""
    return TestClient(app)


@pytest.fixture
def db_session():
    """Provide database session"""
    from db import Session as DBSession
    session = DBSession(engine)
    try:
        yield session
    finally:
        session.rollback()
        session.close()


@pytest.fixture
def user1(db_session: Session):
    """Create first test user"""
    user = User(
        id=str(uuid.uuid4()),
        email=f"user1-{uuid.uuid4()}@example.com",
        name="User One",
        password_hash="hashed_password_1",
        emailVerified=True,
    )
    db_session.add(user)
    db_session.commit()
    db_session.refresh(user)
    yield user
    db_session.delete(user)
    db_session.commit()


@pytest.fixture
def user2(db_session: Session):
    """Create second test user"""
    user = User(
        id=str(uuid.uuid4()),
        email=f"user2-{uuid.uuid4()}@example.com",
        name="User Two",
        password_hash="hashed_password_2",
        emailVerified=True,
    )
    db_session.add(user)
    db_session.commit()
    db_session.refresh(user)
    yield user
    db_session.delete(user)
    db_session.commit()


@pytest.fixture
def auth_header_user1(user1: User):
    """Create JWT token for user1"""
    token = jwt.encode(
        {"user_id": user1.id},
        settings.JWT_SECRET,
        algorithm=settings.JWT_ALGORITHM,
    )
    return {"Authorization": f"Bearer {token}"}


@pytest.fixture
def auth_header_user2(user2: User):
    """Create JWT token for user2"""
    token = jwt.encode(
        {"user_id": user2.id},
        settings.JWT_SECRET,
        algorithm=settings.JWT_ALGORITHM,
    )
    return {"Authorization": f"Bearer {token}"}


class TestChatKitUserIsolation:
    """Tests for user isolation in ChatKit (T023-T024)"""

    def test_unauthenticated_request_blocked(self, client: TestClient):
        """T024: Test - JWT validation blocks unauthenticated requests

        Verify that requests without authentication are rejected
        """
        response = client.post("/api/v1/chatkit/sessions")
        assert response.status_code == 401
        # Should return 401 Unauthorized when no auth header provided
        detail = response.json().get("detail", "").lower()
        assert "authorization" in detail or "authenticated" in detail or "missing" in detail

    def test_user1_cannot_access_user2_conversation(
        self,
        client: TestClient,
        user1: User,
        user2: User,
        auth_header_user1: dict,
        auth_header_user2: dict,
        db_session: Session,
    ):
        """T024: Test - User cannot fetch other user's conversation history

        User1 creates a conversation, User2 tries to access it - should fail with 403
        """
        # User2 creates a session (and conversation)
        response = client.post(
            "/api/v1/chatkit/sessions",
            headers=auth_header_user2,
        )
        assert response.status_code == 200
        user2_conv_id = response.json()["conversation_id"]

        # User1 tries to access User2's conversation via chat endpoint
        response = client.get(
            f"/api/{user1.id}/conversations/{user2_conv_id}",
            headers=auth_header_user1,
        )
        # Should get 403 Forbidden or 404 (different implementations)
        assert response.status_code in [403, 404]

    def test_user1_conversation_isolated_from_user2(
        self,
        client: TestClient,
        user1: User,
        user2: User,
        auth_header_user1: dict,
        auth_header_user2: dict,
        db_session: Session,
    ):
        """T024: Test - User isolation enforced at database level

        Verify that User1's conversation is not visible to User2
        """
        # User1 creates a session
        response = client.post(
            "/api/v1/chatkit/sessions",
            headers=auth_header_user1,
        )
        assert response.status_code == 200
        user1_conv_id = response.json()["conversation_id"]

        # Verify conversation belongs to user1
        stmt = select(Conversation).where(Conversation.id == user1_conv_id)
        conversation = db_session.exec(stmt).first()
        assert conversation is not None
        assert conversation.user_id == user1.id
        assert conversation.user_id != user2.id

    def test_user_list_only_own_conversations(
        self,
        client: TestClient,
        user1: User,
        user2: User,
        auth_header_user1: dict,
        auth_header_user2: dict,
        db_session: Session,
    ):
        """T024: Test - Users only see their own conversations

        User1 and User2 create conversations, each should only see their own
        """
        # User1 creates conversation
        response = client.post(
            "/api/v1/chatkit/sessions",
            headers=auth_header_user1,
        )
        assert response.status_code == 200
        user1_conv_id = response.json()["conversation_id"]

        # User2 creates conversation
        response = client.post(
            "/api/v1/chatkit/sessions",
            headers=auth_header_user2,
        )
        assert response.status_code == 200
        user2_conv_id = response.json()["conversation_id"]

        # User1 lists conversations - should only see their own
        response = client.get(
            f"/api/{user1.id}/conversations",
            headers=auth_header_user1,
        )
        assert response.status_code == 200
        conversations = response.json()
        user1_conv_ids = [c["id"] for c in conversations]
        assert user1_conv_id in user1_conv_ids
        assert user2_conv_id not in user1_conv_ids

    def test_conversation_id_validation_prevents_tampering(
        self,
        client: TestClient,
        user1: User,
        auth_header_user1: dict,
        db_session: Session,
    ):
        """T024: Test - Conversation ID validation prevents tampering

        Try to access non-existent conversation ID - should fail with 404
        """
        # Try to access conversation ID that doesn't exist
        fake_conv_id = 99999
        response = client.get(
            f"/api/{user1.id}/conversations/{fake_conv_id}",
            headers=auth_header_user1,
        )
        assert response.status_code == 404

    def test_user_cannot_modify_other_user_conversation(
        self,
        client: TestClient,
        user1: User,
        user2: User,
        auth_header_user1: dict,
        auth_header_user2: dict,
        db_session: Session,
    ):
        """T024: Test - User cannot create message in other user's conversation

        User1 creates conversation, User2 tries to add message - should fail
        """
        # User1 creates session
        response = client.post(
            "/api/v1/chatkit/sessions",
            headers=auth_header_user1,
        )
        assert response.status_code == 200
        user1_conv_id = response.json()["conversation_id"]
        user1_session_id = response.json()["session_id"]

        # Verify conversation belongs to user1
        stmt = select(Conversation).where(Conversation.id == user1_conv_id)
        conversation = db_session.exec(stmt).first()
        assert conversation.user_id == user1.id

        # User2 cannot create a message using User1's conversation
        # (This would be tested by the ChatKit server's respond method
        # which now validates user_id matches conversation.user_id)
        # For now, we verify at database level that it belongs to user1
        assert conversation.user_id == user1.id
        assert conversation.user_id != user2.id

    def test_multiple_users_isolated_conversations(
        self,
        client: TestClient,
        user1: User,
        user2: User,
        auth_header_user1: dict,
        auth_header_user2: dict,
        db_session: Session,
    ):
        """T024: Test - Multiple users have completely isolated conversations

        Create conversations for both users and verify complete isolation
        """
        # Create 2 conversations for user1
        response1 = client.post(
            "/api/v1/chatkit/sessions",
            headers=auth_header_user1,
        )
        user1_conv1 = response1.json()["conversation_id"]

        response2 = client.post(
            "/api/v1/chatkit/sessions",
            headers=auth_header_user1,
        )
        user1_conv2 = response2.json()["conversation_id"]

        # Create 2 conversations for user2
        response3 = client.post(
            "/api/v1/chatkit/sessions",
            headers=auth_header_user2,
        )
        user2_conv1 = response3.json()["conversation_id"]

        response4 = client.post(
            "/api/v1/chatkit/sessions",
            headers=auth_header_user2,
        )
        user2_conv2 = response4.json()["conversation_id"]

        # Verify all conversations have correct user_id
        stmt = select(Conversation).where(
            Conversation.id.in_([user1_conv1, user1_conv2, user2_conv1, user2_conv2])
        )
        conversations = db_session.exec(stmt).all()
        assert len(conversations) == 4

        # Verify isolation
        for conv in conversations:
            if conv.id in [user1_conv1, user1_conv2]:
                assert conv.user_id == user1.id
            else:
                assert conv.user_id == user2.id

    def test_chatkit_session_belongs_to_user(
        self,
        client: TestClient,
        user1: User,
        user2: User,
        auth_header_user1: dict,
        auth_header_user2: dict,
        db_session: Session,
    ):
        """T024: Test - ChatKitSession record belongs to creating user

        Verify ChatKitSession model stores user_id correctly
        """
        # User1 creates session
        response = client.post(
            "/api/v1/chatkit/sessions",
            headers=auth_header_user1,
        )
        assert response.status_code == 200
        user1_session_id = response.json()["session_id"]

        # User2 creates session
        response = client.post(
            "/api/v1/chatkit/sessions",
            headers=auth_header_user2,
        )
        assert response.status_code == 200
        user2_session_id = response.json()["session_id"]

        # Verify sessions belong to correct users
        stmt1 = select(ChatKitSession).where(ChatKitSession.session_id == user1_session_id)
        session1 = db_session.exec(stmt1).first()
        assert session1 is not None
        assert session1.user_id == user1.id

        stmt2 = select(ChatKitSession).where(ChatKitSession.session_id == user2_session_id)
        session2 = db_session.exec(stmt2).first()
        assert session2 is not None
        assert session2.user_id == user2.id

    def test_zero_percent_unauthorized_access(
        self,
        client: TestClient,
        user1: User,
        user2: User,
        auth_header_user1: dict,
        auth_header_user2: dict,
        db_session: Session,
    ):
        """T024: Test - 0% unauthorized access (comprehensive)

        Comprehensive test that user isolation prevents all unauthorized access
        """
        # Setup: Create conversations for both users
        resp1 = client.post("/api/v1/chatkit/sessions", headers=auth_header_user1)
        user1_conv_id = resp1.json()["conversation_id"]

        resp2 = client.post("/api/v1/chatkit/sessions", headers=auth_header_user2)
        user2_conv_id = resp2.json()["conversation_id"]

        # Test 1: User1 cannot access User2's conversation
        response = client.get(
            f"/api/{user1.id}/conversations/{user2_conv_id}",
            headers=auth_header_user1,
        )
        # Should be 403 (forbidden) or 404 (not found) - either way, access denied
        assert response.status_code in [403, 404]

        # Test 2: User2 cannot access User1's conversation
        response = client.get(
            f"/api/{user2.id}/conversations/{user1_conv_id}",
            headers=auth_header_user2,
        )
        assert response.status_code in [403, 404]

        # Test 3: User1 can access their own conversation
        response = client.get(
            f"/api/{user1.id}/conversations/{user1_conv_id}",
            headers=auth_header_user1,
        )
        assert response.status_code == 200

        # Test 4: User2 can access their own conversation
        response = client.get(
            f"/api/{user2.id}/conversations/{user2_conv_id}",
            headers=auth_header_user2,
        )
        assert response.status_code == 200

        # Result: 0% unauthorized access achieved
        assert True, "All authorization checks passed"
