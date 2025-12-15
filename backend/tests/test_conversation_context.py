"""Tests for Conversation Context Manager

Tests for:
- Loading conversation history
- Context window management
- Message summarization thresholds
- Multi-turn conversation support
"""

import pytest
from sqlmodel import Session, select
from models import Conversation, Message, User
from agents.conversation_context import (
    ConversationContext,
    get_conversation_context,
    MAX_CONTEXT_MESSAGES,
)
from db import engine
from datetime import datetime
import uuid


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
    user = User(
        id=str(uuid.uuid4()),
        email="context-test@example.com",
        name="Context Test User",
        password_hash="hashed_password",
        emailVerified=True,
    )
    db_session.add(user)
    db_session.commit()
    db_session.refresh(user)
    return user


@pytest.fixture
def test_conversation(db_session: Session, test_user: User):
    """Create test conversation"""
    conv = Conversation(
        user_id=test_user.id,
        title="Test Conversation",
        archived=False,
    )
    db_session.add(conv)
    db_session.commit()
    db_session.refresh(conv)
    return conv


@pytest.fixture
def conversation_with_messages(db_session: Session, test_conversation: Conversation):
    """Create conversation with sample messages"""
    messages = []
    for i in range(5):
        msg = Message(
            conversation_id=test_conversation.id,
            user_id=test_conversation.user_id,
            role="user" if i % 2 == 0 else "assistant",
            content=f"Test message {i+1}",
            created_at=datetime.utcnow(),
        )
        db_session.add(msg)
        messages.append(msg)

    db_session.commit()
    return test_conversation


class TestConversationContext:
    """Tests for ConversationContext class"""

    def test_create_context(
        self, test_conversation: Conversation, test_user: User
    ):
        """Test: Create conversation context"""
        # Act
        context = ConversationContext(test_conversation.id, test_user.id)

        # Assert
        assert context.conversation_id == test_conversation.id
        assert context.user_id == test_user.id
        assert isinstance(context.messages, list)

    def test_load_messages_from_database(
        self, conversation_with_messages: Conversation, test_user: User
    ):
        """Test: Load messages from database"""
        # Act
        context = ConversationContext(conversation_with_messages.id, test_user.id)

        # Assert
        assert len(context.messages) == 5
        assert context.messages[0]["role"] == "user"
        assert "Test message 1" in context.messages[0]["content"]

    def test_get_context(
        self, conversation_with_messages: Conversation, test_user: User
    ):
        """Test: Get context for agent"""
        # Arrange
        context = ConversationContext(conversation_with_messages.id, test_user.id)

        # Act
        agent_context = context.get_context()

        # Assert
        assert len(agent_context) <= MAX_CONTEXT_MESSAGES
        assert all("role" in msg for msg in agent_context)
        assert all("content" in msg for msg in agent_context)
        assert all("id" not in msg for msg in agent_context)  # Metadata excluded

    def test_get_context_with_limit(
        self, conversation_with_messages: Conversation, test_user: User
    ):
        """Test: Get context with message limit"""
        # Arrange
        context = ConversationContext(conversation_with_messages.id, test_user.id)

        # Act
        limited_context = context.get_context(max_messages=2)

        # Assert
        assert len(limited_context) <= 2

    def test_get_full_history(
        self, conversation_with_messages: Conversation, test_user: User
    ):
        """Test: Get full conversation history"""
        # Arrange
        context = ConversationContext(conversation_with_messages.id, test_user.id)

        # Act
        full_history = context.get_full_history()

        # Assert
        assert len(full_history) == 5
        assert all("id" in msg for msg in full_history)
        assert all("created_at" in msg for msg in full_history)

    def test_add_message(self, test_conversation: Conversation, test_user: User):
        """Test: Add message to context"""
        # Arrange
        context = ConversationContext(test_conversation.id, test_user.id)

        # Act
        context.add_message(role="user", content="New message")

        # Assert
        assert len(context.messages) == 1
        assert context.messages[0]["role"] == "user"
        assert context.messages[0]["content"] == "New message"

    def test_add_message_with_tool_calls(
        self, test_conversation: Conversation, test_user: User
    ):
        """Test: Add message with tool calls"""
        # Arrange
        context = ConversationContext(test_conversation.id, test_user.id)
        tool_calls = [{"name": "add_task", "result": {"task_id": "123"}}]

        # Act
        context.add_message(
            role="assistant",
            content="Created task",
            tool_calls=tool_calls,
        )

        # Assert
        assert context.messages[0]["tool_calls"] == tool_calls

    def test_get_message_count(
        self, conversation_with_messages: Conversation, test_user: User
    ):
        """Test: Get message count"""
        # Act
        context = ConversationContext(conversation_with_messages.id, test_user.id)
        count = context.get_message_count()

        # Assert
        assert count == 5

    def test_get_summary(
        self, conversation_with_messages: Conversation, test_user: User
    ):
        """Test: Get conversation summary"""
        # Arrange
        context = ConversationContext(conversation_with_messages.id, test_user.id)

        # Act
        summary = context.get_summary()

        # Assert
        assert "Conversation with 5 messages" in summary
        assert "task management" in summary.lower()

    def test_clear_context(
        self, conversation_with_messages: Conversation, test_user: User
    ):
        """Test: Clear context (cache only, not database)"""
        # Arrange
        context = ConversationContext(conversation_with_messages.id, test_user.id)
        assert context.get_message_count() == 5

        # Act
        context.clear()

        # Assert
        assert context.get_message_count() == 0

    def test_repr(self, test_conversation: Conversation, test_user: User):
        """Test: String representation"""
        # Act
        context = ConversationContext(test_conversation.id, test_user.id)

        # Assert
        repr_str = repr(context)
        assert f"conversation_id={test_conversation.id}" in repr_str
        assert "messages=0" in repr_str


class TestConversationContextFactory:
    """Tests for get_conversation_context factory function"""

    def test_factory_function(
        self, test_conversation: Conversation, test_user: User
    ):
        """Test: Factory function creates context"""
        # Act
        context = get_conversation_context(test_conversation.id, test_user.id)

        # Assert
        assert isinstance(context, ConversationContext)
        assert context.conversation_id == test_conversation.id
        assert context.user_id == test_user.id


class TestMultiTurnConversation:
    """Tests for multi-turn conversation support"""

    def test_multi_turn_context_building(
        self, test_conversation: Conversation, test_user: User, db_session: Session
    ):
        """Test: Build multi-turn context from conversation"""
        # Arrange - Add messages
        messages_data = [
            ("user", "Add a task to buy groceries"),
            ("assistant", "I've added 'Buy groceries' to your task list"),
            ("user", "Show my pending tasks"),
            ("assistant", "You have 1 pending task: Buy groceries"),
            ("user", "Mark it as complete"),
            ("assistant", "I've marked 'Buy groceries' as complete! ✓"),
        ]

        for role, content in messages_data:
            msg = Message(
                conversation_id=test_conversation.id,
                user_id=test_conversation.user_id,
                role=role,
                content=content,
            )
            db_session.add(msg)

        db_session.commit()

        # Act
        context = ConversationContext(test_conversation.id, test_user.id)
        agent_context = context.get_context()

        # Assert
        assert len(agent_context) == 6
        assert agent_context[0]["role"] == "user"
        assert "buy groceries" in agent_context[0]["content"].lower()
        assert agent_context[-1]["role"] == "assistant"

    def test_context_window_truncation(
        self, test_conversation: Conversation, test_user: User, db_session: Session
    ):
        """Test: Context window limits recent messages"""
        # Arrange - Add many messages
        for i in range(MAX_CONTEXT_MESSAGES + 5):
            msg = Message(
                conversation_id=test_conversation.id,
                user_id=test_conversation.user_id,
                role="user" if i % 2 == 0 else "assistant",
                content=f"Message {i+1}",
            )
            db_session.add(msg)

        db_session.commit()

        # Act
        context = ConversationContext(test_conversation.id, test_user.id)
        agent_context = context.get_context()

        # Assert
        assert len(agent_context) == MAX_CONTEXT_MESSAGES
        # Should include most recent messages
        assert "Message 25" in agent_context[-1]["content"]

    def test_conversation_history_ordering(
        self, test_conversation: Conversation, test_user: User, db_session: Session
    ):
        """Test: Messages are ordered by creation time"""
        # Arrange
        for i in range(3):
            msg = Message(
                conversation_id=test_conversation.id,
                user_id=test_conversation.user_id,
                role="user",
                content=f"Message {i+1}",
            )
            db_session.add(msg)

        db_session.commit()

        # Act
        context = ConversationContext(test_conversation.id, test_user.id)

        # Assert
        assert context.messages[0]["content"] == "Message 1"
        assert context.messages[1]["content"] == "Message 2"
        assert context.messages[2]["content"] == "Message 3"

    def test_conversation_summary_with_tasks(
        self, test_conversation: Conversation, test_user: User, db_session: Session
    ):
        """Test: Summary identifies task-related conversations"""
        # Arrange - Add task-related messages
        messages = [
            "Add a task to buy groceries",
            "Update the task description",
            "Complete the groceries task",
            "Delete the old task",
        ]

        for msg_content in messages:
            msg = Message(
                conversation_id=test_conversation.id,
                user_id=test_conversation.user_id,
                role="user",
                content=msg_content,
            )
            db_session.add(msg)

        db_session.commit()

        # Act
        context = ConversationContext(test_conversation.id, test_user.id)
        summary = context.get_summary()

        # Assert
        assert "task management" in summary.lower()
        assert "4 messages" in summary
