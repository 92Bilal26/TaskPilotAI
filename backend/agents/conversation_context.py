"""Conversation Context Manager

Manages conversation history and context for multi-turn interactions.
Implements context window management and message summarization.
"""

import logging
from typing import List, Dict, Any, Optional
from sqlmodel import Session, select
from db import engine
from models import Message

logger = logging.getLogger(__name__)

# Context window limits
MAX_CONTEXT_MESSAGES = 20  # Maximum messages to keep in context
CONTEXT_WINDOW_SIZE = 8000  # Maximum tokens in context (approximate)
SUMMARIZE_THRESHOLD = 20  # Summarize after this many messages


class ConversationContext:
    """Manages conversation history and context"""

    def __init__(self, conversation_id: int, user_id: str):
        """Initialize conversation context

        Args:
            conversation_id: ID of the conversation
            user_id: ID of the user
        """
        self.conversation_id = conversation_id
        self.user_id = user_id
        self.messages: List[Dict[str, Any]] = []
        self._load_messages()

    def _load_messages(self) -> None:
        """Load conversation messages from database"""
        try:
            with Session(engine) as session:
                query = select(Message).where(
                    Message.conversation_id == self.conversation_id
                ).order_by(Message.created_at)

                db_messages = session.exec(query).all()

                # Convert to message format for agent
                self.messages = [
                    {
                        "role": msg.role,
                        "content": msg.content,
                        "id": msg.id,
                        "created_at": msg.created_at.isoformat(),
                        "tool_calls": msg.tool_calls,
                    }
                    for msg in db_messages
                ]

                logger.info(
                    f"Loaded {len(self.messages)} messages for conversation {self.conversation_id}"
                )
        except Exception as e:
            logger.error(f"Failed to load conversation messages: {e}")
            self.messages = []

    def get_context(self, max_messages: Optional[int] = None) -> List[Dict[str, str]]:
        """Get conversation context for agent

        Args:
            max_messages: Maximum number of recent messages to include

        Returns:
            List of message dicts with role and content
        """
        max_msgs = max_messages or MAX_CONTEXT_MESSAGES

        # Return last N messages, excluding tool_calls and metadata
        context_messages = self.messages[-max_msgs:]

        return [
            {"role": msg["role"], "content": msg["content"]}
            for msg in context_messages
        ]

    def get_full_history(self) -> List[Dict[str, Any]]:
        """Get full conversation history with metadata

        Returns:
            List of all messages with metadata
        """
        return self.messages.copy()

    def add_message(
        self,
        role: str,
        content: str,
        tool_calls: Optional[Dict[str, Any]] = None,
    ) -> None:
        """Add message to context

        Args:
            role: Message role ('user' or 'assistant')
            content: Message content
            tool_calls: Optional tool calls data
        """
        message = {
            "role": role,
            "content": content,
            "tool_calls": tool_calls,
            "created_at": None,  # Set by database
        }
        self.messages.append(message)

        # Check if summarization needed
        if len(self.messages) >= SUMMARIZE_THRESHOLD:
            self._maybe_summarize()

    def _maybe_summarize(self) -> None:
        """Summarize old messages if context is too large

        This is a placeholder for context window management.
        In a real implementation, this would:
        1. Identify old message groups
        2. Call LLM to create summary
        3. Replace old messages with summary
        """
        logger.warning(
            f"Conversation {self.conversation_id} has {len(self.messages)} messages. "
            f"Consider implementing message summarization."
        )

    def get_message_count(self) -> int:
        """Get total number of messages in conversation

        Returns:
            Number of messages
        """
        return len(self.messages)

    def get_summary(self) -> str:
        """Get a summary of the conversation for context

        Returns:
            Brief summary of conversation topics
        """
        if not self.messages:
            return "Empty conversation"

        # Count message types
        user_msgs = sum(1 for m in self.messages if m["role"] == "user")
        assistant_msgs = sum(1 for m in self.messages if m["role"] == "assistant")

        # Identify tasks mentioned
        task_count = 0
        for msg in self.messages:
            if any(
                keyword in msg["content"].lower()
                for keyword in ["task", "todo", "add", "complete", "delete"]
            ):
                task_count += 1

        summary = (
            f"Conversation with {len(self.messages)} messages "
            f"({user_msgs} from user, {assistant_msgs} from assistant). "
            f"Topics: task management."
        )

        return summary

    def clear(self) -> None:
        """Clear conversation context

        WARNING: This does NOT delete from database, just clears cache.
        """
        self.messages = []
        logger.info(f"Cleared context for conversation {self.conversation_id}")

    def __repr__(self) -> str:
        return (
            f"ConversationContext("
            f"conversation_id={self.conversation_id}, "
            f"messages={len(self.messages)})"
        )


def get_conversation_context(
    conversation_id: int,
    user_id: str,
) -> ConversationContext:
    """Factory function to create conversation context

    Args:
        conversation_id: ID of conversation
        user_id: ID of user

    Returns:
        Initialized ConversationContext
    """
    logger.info(f"Creating context for conversation {conversation_id}")
    return ConversationContext(conversation_id, user_id)
