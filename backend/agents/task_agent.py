"""Task Agent using OpenAI Agents SDK

This module initializes and manages the task agent that processes natural language
requests and coordinates MCP tool execution for task management.
"""

import logging
from typing import Any, Optional

logger = logging.getLogger(__name__)


class TaskAgent:
    """Agent for processing natural language task management requests

    Uses OpenAI Agents SDK to:
    1. Accept natural language messages from users
    2. Select appropriate MCP tools based on user intent
    3. Execute tools and return results
    4. Generate natural language responses
    """

    def __init__(self, api_key: str):
        """Initialize TaskAgent with OpenAI API key

        Args:
            api_key: OpenAI API key for Agents SDK

        Raises:
            ValueError: If api_key is not provided
        """
        if not api_key:
            raise ValueError("OpenAI API key is required")

        self.api_key = api_key
        self.tools: dict[str, Any] = {}
        logger.info("TaskAgent initialized")

    def register_tool(self, name: str, tool: Any) -> None:
        """Register an MCP tool with the agent

        Args:
            name: Tool name (e.g., 'add_task', 'list_tasks')
            tool: Tool implementation
        """
        self.tools[name] = tool
        logger.info(f"Tool registered with agent: {name}")

    def get_available_tools(self) -> list[str]:
        """Get list of available tools

        Returns:
            List of tool names
        """
        return list(self.tools.keys())

    async def process_message(
        self,
        user_id: str,
        message: str,
        conversation_history: Optional[list[dict[str, str]]] = None,
    ) -> dict[str, Any]:
        """Process a user message and generate response

        Args:
            user_id: User ID from JWT token
            message: User's natural language message
            conversation_history: Previous messages in conversation

        Returns:
            Dictionary with:
            - response: Natural language response from agent
            - tool_calls: List of tools that were invoked
            - status: 'success' or 'error'
        """
        logger.info(f"Processing message from user {user_id}: {message}")

        try:
            # Build conversation history for context
            messages = conversation_history or []
            messages.append({"role": "user", "content": message})

            # Call OpenAI with tools
            response = self._call_openai_with_tools(
                user_id=user_id,
                messages=messages,
            )

            return response

        except Exception as e:
            logger.error(f"Error processing message: {e}")
            return {
                "response": f"I encountered an error: {str(e)}",
                "tool_calls": [],
                "status": "error",
            }

    def _call_openai_with_tools(
        self,
        user_id: str,
        messages: list[dict[str, str]],
    ) -> dict[str, Any]:
        """Call OpenAI API with available tools

        Args:
            user_id: User ID for context
            messages: Conversation history

        Returns:
            Response with tool calls and assistant message
        """
        logger.info(f"Calling OpenAI API with {len(self.tools)} tools")

        # Placeholder: This would call OpenAI API
        # For now, return a simple response
        return {
            "response": "I received your message and can help you with task management",
            "tool_calls": [],
            "status": "pending",
        }


def initialize_task_agent(api_key: str) -> TaskAgent:
    """Initialize and return configured TaskAgent

    Args:
        api_key: OpenAI API key

    Returns:
        Configured TaskAgent instance

    Raises:
        ValueError: If api_key is invalid
    """
    logger.info("Initializing TaskAgent")
    agent = TaskAgent(api_key=api_key)

    # Tools will be registered here as they are implemented
    # This is a placeholder for Phase 2 infrastructure

    return agent
