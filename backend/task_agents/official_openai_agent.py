"""Official OpenAI Agents SDK Implementation

This module uses the official OpenAI Agents SDK as documented at:
https://openai.github.io/openai-agents-python/

Key Features:
- Agent: LLM equipped with instructions and tools
- Runner: Executes the agent loop
- Tools: Python functions converted to tools automatically
- Sessions: Automatic conversation history management
"""

import logging
from typing import Any, Optional, Callable, Dict
from agents import Agent, Runner, set_default_openai_key  # Official OpenAI Agents SDK
from agents.tool import function_tool  # Wrapper for tool functions
from config import settings

logger = logging.getLogger(__name__)


class TaskManagementAgent:
    """
    Official OpenAI Agents SDK implementation for task management.

    Uses the lightweight, production-ready framework from:
    https://openai.github.io/openai-agents-python/

    Architecture:
    - Agent: Equipped with task management instructions
    - Tools: Python functions (add_task, delete_task, etc.)
    - Runner: Built-in agent loop (no manual iteration needed)
    - Session: Automatic conversation history
    """

    def __init__(self, tools: Optional[list[Callable]] = None):
        """Initialize the task management agent with official SDK

        Args:
            tools: Optional list of tool functions to register

        Raises:
            ValueError: If OpenAI API key is not configured
        """
        # Validate API key
        api_key = settings.OPENAI_API_KEY
        if not api_key or api_key == "sk-test-key":
            raise ValueError("OPENAI_API_KEY must be set in environment")

        # Set default OpenAI API key for the agents SDK
        set_default_openai_key(api_key)

        # Agent instructions for multi-step task operations
        instructions = """You are TaskPilot AI, a helpful task management assistant powered by OpenAI.

You have access to tools for managing tasks. When users ask you to manage tasks, use the appropriate tools.

IMPORTANT WORKFLOW:
1. When a user mentions a task by name (e.g., "delete task buy milk"):
   - First use find_task_by_name() to locate the task and get its ID
   - Then use delete_task(), complete_task(), or update_task() with that ID
   - Finally, confirm the action with the task title

2. For listing tasks:
   - Use list_tasks() to retrieve all tasks
   - Display them in a clear, readable format with status indicators

3. For adding tasks:
   - Use add_task() with clear title and optional description
   - Confirm the newly created task

4. Always provide clear confirmations:
   - "I've added 'Buy milk' to your tasks ✓"
   - "I've deleted 'Buy milk' from your tasks ✓"
   - "I've marked 'Buy milk' as complete ✓"

Multi-step example:
- User: "delete task buy milk"
- You: (1) Call find_task_by_name("buy milk") → get ID
- You: (2) Call delete_task(id) → delete it
- You: (3) Respond: "I've deleted 'Buy milk' ✓"

Be helpful, clear, and confirm all actions."""

        # Wrap tools with function_tool decorator for official SDK compatibility
        wrapped_tools = [function_tool(tool) for tool in (tools or [])]

        # Create agent with official SDK
        # Pass tools upfront if provided, otherwise use empty list
        self.agent = Agent(
            name="TaskPilot AI",
            instructions=instructions,
            model="gpt-4-turbo-preview",  # Latest model
            tools=wrapped_tools,  # Initialize with wrapped tools
        )

        # Dictionary to store registered tools
        self.tools: Dict[str, Callable] = {}

        logger.info("TaskManagementAgent initialized with official OpenAI Agents SDK")

    def register_tool(self, name: str, tool_func: Callable) -> None:
        """
        Register a tool with the agent.

        The official SDK automatically:
        - Extracts function signature
        - Generates OpenAI tool schema from type hints
        - Handles tool calling and result processing

        Args:
            name: Tool name (e.g., 'add_task', 'delete_task')
            tool_func: Python function implementing the tool
        """
        self.tools[name] = tool_func

        # Register with agent - wrap with function_tool for SDK compatibility
        # The SDK uses function_tool wrapper to handle tool introspection
        wrapped_tool = function_tool(tool_func)
        self.agent.tools.append(wrapped_tool)

        logger.info(f"Tool registered: {name}")

    def get_available_tools(self) -> list[str]:
        """Get list of registered tool names

        Returns:
            List of tool function names
        """
        return list(self.tools.keys())

    async def process_message(
        self,
        user_id: str,
        message: str,
        conversation_history: Optional[list[Dict[str, str]]] = None,
    ) -> Dict[str, Any]:
        """
        Process a user message using the official OpenAI Agents SDK.

        The SDK handles:
        - Tool selection based on user intent
        - Tool execution with automatic retry
        - Result processing and response generation
        - Conversation memory management

        Args:
            user_id: User ID for context
            message: User's natural language message
            conversation_history: Previous conversation messages

        Returns:
            Dictionary with:
            - response: Final response from the agent
            - tool_calls: Tools that were called (for logging)
            - status: 'success' or 'error'
        """
        logger.info(f"Processing message from user {user_id}: {message[:50]}...")

        try:
            # Add user_id to message context for tools
            # Tools can access this via context
            augmented_message = f"[User ID: {user_id}] {message}"

            # The official SDK's Runner handles the entire agent loop
            # No manual iteration needed - it's all built-in
            # Runner automatically:
            # - Calls the LLM
            # - Selects appropriate tools
            # - Executes tools
            # - Feeds results back to LLM
            # - Loops until task is complete
            result = await Runner.run(
                self.agent,
                augmented_message,
            )

            # Extract response
            final_response = result.final_output if hasattr(result, 'final_output') else str(result)

            # Get tool calls (if available)
            tool_calls = []
            if hasattr(result, 'messages'):
                # Extract tool call information from messages
                for msg in result.messages:
                    if hasattr(msg, 'tool_calls') and msg.tool_calls:
                        for tool_call in msg.tool_calls:
                            tool_calls.append({
                                "name": tool_call.function.name if hasattr(tool_call, 'function') else "unknown",
                                "status": "executed",
                            })

            logger.info(f"Agent completed message processing. Tools called: {len(tool_calls)}")

            return {
                "response": final_response,
                "tool_calls": tool_calls,
                "status": "success",
            }

        except Exception as e:
            logger.error(f"Error processing message: {e}")
            return {
                "response": f"I encountered an error: {str(e)}",
                "tool_calls": [],
                "status": "error",
            }


def create_task_agent(tools: Optional[list[Callable]] = None) -> TaskManagementAgent:
    """
    Factory function to create and configure a task management agent.

    Args:
        tools: Optional list of tool functions to register with the agent

    Returns:
        Configured TaskManagementAgent instance

    Raises:
        ValueError: If OpenAI API key is not configured
    """
    logger.info("Creating TaskManagementAgent with official OpenAI Agents SDK")
    agent = TaskManagementAgent(tools=tools)
    return agent
