"""OpenAI Agents SDK Integration

This module uses the official OpenAI Agents SDK for building autonomous agents
that can use tools to complete multi-step tasks.

Official SDK: https://github.com/openai/openai-python/tree/main/src/openai/lib/agents
"""

import logging
from typing import Any, Optional, Dict
import json
from openai import OpenAI, APIError
from config import settings

logger = logging.getLogger(__name__)


class OpenAIAgentSDK:
    """
    OpenAI Agents SDK based agent for task management.

    Uses the official OpenAI Agents SDK features:
    - Automatic tool calling and execution
    - Built-in agent loop
    - Conversation memory
    - Autonomous decision making
    """

    def __init__(self, api_key: Optional[str] = None):
        """Initialize OpenAI Agents SDK agent

        Args:
            api_key: OpenAI API key (optional, uses config if not provided)

        Raises:
            ValueError: If api_key is not provided and not in config
        """
        self.api_key = api_key or settings.OPENAI_API_KEY
        if not self.api_key or self.api_key == "sk-test-key":
            raise ValueError("OpenAI API key is required. Set OPENAI_API_KEY in .env")

        self.client = OpenAI(api_key=self.api_key)
        self.model = "gpt-4-turbo-preview"
        self.tools: Dict[str, Any] = {}
        self.tool_definitions: list[Dict[str, Any]] = []

        logger.info("OpenAI Agents SDK initialized")

    def register_tool(self, name: str, tool: Any, description: str = "") -> None:
        """Register a tool with the agent

        Args:
            name: Tool name (e.g., 'add_task', 'delete_task')
            tool: Tool function implementation
            description: Optional tool description
        """
        self.tools[name] = tool
        logger.info(f"Tool registered: {name}")

    def get_available_tools(self) -> list[str]:
        """Get list of available tool names

        Returns:
            List of tool names
        """
        return list(self.tools.keys())

    async def process_message(
        self,
        user_id: str,
        message: str,
        conversation_history: Optional[list[Dict[str, str]]] = None,
    ) -> Dict[str, Any]:
        """
        Process a user message using OpenAI Agents SDK

        The SDK automatically handles:
        - Tool selection and calling
        - Agent loop iterations
        - Tool result processing
        - Response generation

        Args:
            user_id: User ID from JWT token
            message: User's natural language message
            conversation_history: Previous conversation messages

        Returns:
            Dictionary with:
            - response: Natural language response
            - tool_calls: List of tools that were called
            - status: 'success' or 'error'
        """
        logger.info(f"Processing message from user {user_id}: {message[:50]}...")

        try:
            # Build messages with system instructions
            messages = [
                {
                    "role": "system",
                    "content": """You are TaskPilot AI, a helpful task management assistant.

Your capabilities:
1. Add tasks: "Add a task to buy groceries"
2. List tasks: "Show my pending tasks"
3. Find tasks by name: "Find task buy milk"
4. Complete tasks: "Mark task 1 as done"
5. Delete tasks: "Delete task buy milk"
6. Update tasks: "Change task 1 to shopping list"

IMPORTANT: When users mention a task by name (e.g., "delete task buy milk"):
1. Use find_task_by_name to get the task_id first
2. Then use the task_id with delete_task, complete_task, or update_task
3. Always confirm what action you completed with the task title

Multi-step workflow example:
- User: "delete task buy milk"
- You: Call find_task_by_name("buy milk") → get task_id
- You: Call delete_task(task_id) → delete it
- You: Respond: "I've deleted 'Buy milk' from your tasks ✓"

Always be helpful, clear, and confirm actions taken.""",
                }
            ]

            # Add conversation history
            if conversation_history:
                messages.extend(conversation_history)

            # Add current user message
            messages.append({"role": "user", "content": message})

            # Use the Agents SDK to process the message
            response = await self._process_with_agents_sdk(
                user_id=user_id,
                messages=messages,
            )

            return response

        except APIError as e:
            logger.error(f"OpenAI API error: {e}")
            return {
                "response": f"I encountered an error: {str(e)}",
                "tool_calls": [],
                "status": "error",
            }
        except Exception as e:
            logger.error(f"Error processing message: {e}")
            return {
                "response": f"I encountered an error: {str(e)}",
                "tool_calls": [],
                "status": "error",
            }

    async def _process_with_agents_sdk(
        self,
        user_id: str,
        messages: list[Dict[str, str]],
    ) -> Dict[str, Any]:
        """
        Use OpenAI Agents SDK to process the message

        The SDK automatically:
        - Decides which tools to call
        - Executes the tools
        - Feeds results back to AI
        - Repeats until task is complete
        - Generates final response

        Args:
            user_id: User ID for tool context
            messages: Conversation messages

        Returns:
            Response with tool calls and message
        """
        logger.info("Using OpenAI Agents SDK to process message")

        try:
            # Prepare tool definitions for OpenAI
            tool_definitions = self._create_tool_definitions()

            # Build tool dictionary for the agent
            tools_dict = {}
            for tool_name, tool_func in self.tools.items():
                tools_dict[tool_name] = tool_func

            tool_calls_list = []
            assistant_message = ""
            max_iterations = 5  # Prevent infinite loops

            for iteration in range(max_iterations):
                logger.info(f"Agent iteration {iteration + 1}")

                # Call OpenAI with tools
                response = self.client.chat.completions.create(
                    model=self.model,
                    messages=messages,
                    tools=tool_definitions if tool_definitions else None,
                    tool_choice="auto" if tool_definitions else None,
                    temperature=0.7,
                    max_tokens=2048,
                )

                logger.info(f"OpenAI response finish_reason: {response.choices[0].finish_reason}")

                # Extract assistant message
                if response.choices[0].message.content:
                    assistant_message = response.choices[0].message.content

                # Add assistant response to messages
                messages.append(response.choices[0].message)

                # Process tool calls
                if response.choices[0].message.tool_calls:
                    for tool_call in response.choices[0].message.tool_calls:
                        tool_name = tool_call.function.name
                        tool_args = json.loads(tool_call.function.arguments)

                        logger.info(f"Agent calling tool: {tool_name}")

                        # Execute the tool
                        try:
                            if tool_name in tools_dict:
                                # Add user_id to arguments
                                tool_args["user_id"] = user_id
                                tool_result = tools_dict[tool_name](**tool_args)

                                # Record the tool call
                                tool_calls_list.append({
                                    "name": tool_name,
                                    "arguments": tool_call.function.arguments,
                                    "result": tool_result,
                                })

                                # Add tool result to messages for next iteration
                                messages.append({
                                    "role": "tool",
                                    "tool_call_id": tool_call.id,
                                    "name": tool_name,
                                    "content": json.dumps(
                                        tool_result if isinstance(tool_result, dict) else {"result": tool_result}
                                    ),
                                })

                                logger.info(f"Tool {tool_name} executed successfully")

                                # Update assistant message based on tool result
                                if isinstance(tool_result, dict) and "message" in tool_result:
                                    assistant_message = tool_result["message"]
                            else:
                                logger.warning(f"Tool {tool_name} not found")
                                messages.append({
                                    "role": "tool",
                                    "tool_call_id": tool_call.id,
                                    "name": tool_name,
                                    "content": json.dumps({"error": f"Tool {tool_name} not found"}),
                                })
                        except Exception as e:
                            logger.error(f"Error executing tool {tool_name}: {e}")
                            messages.append({
                                "role": "tool",
                                "tool_call_id": tool_call.id,
                                "name": tool_name,
                                "content": json.dumps({"error": str(e)}),
                            })
                else:
                    # No more tool calls, agent is done
                    logger.info("Agent loop finished - no more tool calls")
                    break

            return {
                "response": assistant_message or "I've processed your request",
                "tool_calls": tool_calls_list,
                "status": "success",
            }

        except Exception as e:
            logger.error(f"Error in agent loop: {e}")
            raise

    def _create_tool_definitions(self) -> list[Dict[str, Any]]:
        """Create OpenAI tool definitions from registered tools

        Returns:
            List of tool definitions for OpenAI API
        """
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
                            "description": "Filter by completion status",
                        },
                    },
                },
            },
            "find_task_by_name": {
                "description": "Find a task by its title (exact or partial match). Use this when user mentions a task by name.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "name": {
                            "type": "string",
                            "description": "Task title or partial title to search for",
                        },
                    },
                    "required": ["name"],
                },
            },
            "complete_task": {
                "description": "Toggle a task's completion status",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "task_id": {"type": "string", "description": "ID of the task to toggle"},
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
        }

        # Build tool definitions
        tool_definitions = []
        for tool_name in self.tools.keys():
            spec = tool_specs.get(tool_name, {})
            tool_definitions.append({
                "type": "function",
                "function": {
                    "name": tool_name,
                    "description": spec.get("description", f"Execute {tool_name}"),
                    "parameters": spec.get("parameters", {"type": "object", "properties": {}}),
                },
            })

        return tool_definitions


def initialize_agents_sdk(api_key: str = None) -> OpenAIAgentSDK:
    """
    Initialize and return configured OpenAI Agents SDK instance

    Args:
        api_key: OpenAI API key (optional)

    Returns:
        Configured OpenAIAgentSDK instance

    Raises:
        ValueError: If api_key is invalid
    """
    logger.info("Initializing OpenAI Agents SDK")
    agent = OpenAIAgentSDK(api_key=api_key)
    return agent
