"""Task Agent using OpenAI Agents SDK

This module initializes and manages the task agent that processes natural language
requests and coordinates MCP tool execution for task management.
"""

import logging
from typing import Any, Optional
import json
from openai import OpenAI
from config import settings

logger = logging.getLogger(__name__)


class TaskAgent:
    """Agent for processing natural language task management requests

    Uses OpenAI Agents SDK to:
    1. Accept natural language messages from users
    2. Select appropriate MCP tools based on user intent
    3. Execute tools and return results
    4. Generate natural language responses
    """

    def __init__(self, api_key: Optional[str] = None):
        """Initialize TaskAgent with OpenAI API key

        Args:
            api_key: OpenAI API key for Agents SDK (optional, uses config if not provided)

        Raises:
            ValueError: If api_key is not provided and not in config
        """
        self.api_key = api_key or settings.OPENAI_API_KEY
        if not self.api_key or self.api_key == "sk-test-key":
            raise ValueError("OpenAI API key is required. Set OPENAI_API_KEY in .env")

        self.client = OpenAI(api_key=self.api_key)
        self.tools: dict[str, Any] = {}
        self.tool_definitions: list[dict[str, Any]] = []
        logger.info("TaskAgent initialized with OpenAI API")

    def register_tool(self, name: str, tool: Any) -> None:
        """Register an MCP tool with the agent

        Args:
            name: Tool name (e.g., 'add_task', 'list_tasks')
            tool: Tool implementation (callable function)
        """
        self.tools[name] = tool

        # Create tool definition for OpenAI
        tool_def = self._create_tool_definition(name, tool)
        self.tool_definitions.append(tool_def)

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

    def _create_tool_definition(self, name: str, tool: Any) -> dict[str, Any]:
        """Create OpenAI tool definition from function

        Args:
            name: Tool name
            tool: Tool function

        Returns:
            Tool definition for OpenAI API
        """
        # Map tool names to descriptions and parameters
        tool_specs = {
            "add_task": {
                "description": "Create a new task with title and optional description",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "title": {"type": "string", "description": "Task title (1-200 chars)"},
                        "description": {
                            "type": "string",
                            "description": "Optional task description (max 1000 chars)",
                        },
                    },
                    "required": ["title"],
                },
            },
            "list_tasks": {
                "description": "Retrieve user's tasks with optional filtering by status",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "status": {
                            "type": "string",
                            "enum": ["all", "pending", "completed"],
                            "description": "Filter tasks by completion status",
                        },
                    },
                },
            },
            "complete_task": {
                "description": "Toggle a task's completion status (mark complete or uncomplete)",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "task_id": {"type": "string", "description": "ID of the task to toggle"},
                    },
                    "required": ["task_id"],
                },
            },
            "update_task": {
                "description": "Update a task's title and/or description",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "task_id": {"type": "string", "description": "ID of the task to update"},
                        "title": {"type": "string", "description": "New task title"},
                        "description": {"type": "string", "description": "New task description"},
                    },
                    "required": ["task_id"],
                },
            },
            "delete_task": {
                "description": "Permanently delete a task",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "task_id": {"type": "string", "description": "ID of the task to delete"},
                    },
                    "required": ["task_id"],
                },
            },
        }

        spec = tool_specs.get(name, {})

        return {
            "type": "function",
            "function": {
                "name": name,
                "description": spec.get("description", f"Execute {name} tool"),
                "parameters": spec.get(
                    "parameters",
                    {"type": "object", "properties": {}},
                ),
            },
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

        try:
            # Call OpenAI with tools
            response = self.client.chat.completions.create(
                model="gpt-4-turbo-preview",
                messages=messages,
                tools=self.tool_definitions if self.tool_definitions else None,
                tool_choice="auto" if self.tool_definitions else None,
            )

            logger.info(f"OpenAI response: {response.choices[0].finish_reason}")

            # Extract response content
            assistant_message = response.choices[0].message.content or ""

            # Process tool calls if any
            tool_calls = []
            if response.choices[0].message.tool_calls:
                for tool_call in response.choices[0].message.tool_calls:
                    tool_name = tool_call.function.name
                    tool_args = json.loads(tool_call.function.arguments)

                    # Execute tool
                    try:
                        if tool_name in self.tools:
                            # Add user_id to arguments
                            tool_args["user_id"] = user_id
                            result = self.tools[tool_name](**tool_args)

                            tool_calls.append(
                                {
                                    "name": tool_name,
                                    "arguments": tool_call.function.arguments,
                                    "result": result,
                                }
                            )

                            # Extract message from tool result
                            if isinstance(result, dict) and "message" in result:
                                assistant_message = result["message"]

                            logger.info(f"Tool {tool_name} executed successfully")
                        else:
                            logger.warning(f"Tool {tool_name} not found")
                    except Exception as e:
                        logger.error(f"Error executing tool {tool_name}: {e}")
                        tool_calls.append(
                            {
                                "name": tool_name,
                                "arguments": tool_call.function.arguments,
                                "error": str(e),
                            }
                        )

            return {
                "response": assistant_message or "I've processed your request",
                "tool_calls": tool_calls,
                "status": "success",
            }

        except Exception as e:
            logger.error(f"OpenAI API error: {e}")
            return {
                "response": f"I encountered an error: {str(e)}",
                "tool_calls": [],
                "status": "error",
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
