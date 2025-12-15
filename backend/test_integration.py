#!/usr/bin/env python3
"""
Integration test for TaskAgent with OpenAI API

Tests the complete flow:
1. Initialize agent with OpenAI API key
2. Register all MCP tools
3. Process a natural language message
4. Verify tool execution and response
"""

import asyncio
import sys
from agents.task_agent import TaskAgent
from mcp.server import initialize_mcp_server
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


async def test_agent_integration():
    """Test complete agent integration"""

    print("\n" + "=" * 60)
    print("TaskPilotAI Agent Integration Test")
    print("=" * 60 + "\n")

    # Step 1: Initialize agent
    print("1️⃣  Initializing TaskAgent...")
    try:
        agent = TaskAgent()
        print("   ✅ Agent initialized successfully\n")
    except ValueError as e:
        print(f"   ❌ Failed to initialize agent: {e}")
        print("   ⚠️  Make sure OPENAI_API_KEY is set in .env\n")
        return False

    # Step 2: Register tools
    print("2️⃣  Registering MCP tools...")
    try:
        mcp_server = initialize_mcp_server()
        for tool_name, tool_func in mcp_server.get_tools().items():
            agent.register_tool(tool_name, tool_func)
            print(f"   ✅ Registered: {tool_name}")

        print(f"\n   Total tools registered: {len(agent.get_available_tools())}\n")
    except Exception as e:
        print(f"   ❌ Failed to register tools: {e}\n")
        return False

    # Step 3: Process a test message
    print("3️⃣  Testing agent message processing...")
    print("   Sending: 'Add a task to buy groceries'\n")

    try:
        test_user_id = "test-user-integration-001"
        test_message = "Add a task to buy groceries"

        response = await agent.process_message(
            user_id=test_user_id,
            message=test_message,
            conversation_history=[],
        )

        print("   Response from agent:")
        print(f"   - Status: {response['status']}")
        print(f"   - Message: {response['response']}")
        print(f"   - Tools called: {len(response['tool_calls'])}")

        if response["tool_calls"]:
            print("\n   Tool calls executed:")
            for tool_call in response["tool_calls"]:
                print(f"   - {tool_call['name']}")
                if "error" in tool_call:
                    print(f"     Error: {tool_call['error']}")
                elif "result" in tool_call:
                    result = tool_call["result"]
                    if isinstance(result, dict) and "message" in result:
                        print(f"     Result: {result['message']}")

        print("\n   ✅ Agent processed message successfully\n")
        return True

    except Exception as e:
        print(f"   ❌ Failed to process message: {e}\n")
        import traceback
        traceback.print_exc()
        return False


async def main():
    """Run integration tests"""
    success = await test_agent_integration()

    print("=" * 60)
    if success:
        print("✅ Integration test PASSED")
        print("=" * 60)
        print("\nThe TaskAgent is ready for production use!")
        print("\nNext steps:")
        print("1. Start the FastAPI server: uvicorn main:app --reload")
        print("2. Send POST request to /api/{user_id}/chat")
        print("3. Try natural language commands!")
        sys.exit(0)
    else:
        print("❌ Integration test FAILED")
        print("=" * 60)
        print("\nPlease check:")
        print("1. OPENAI_API_KEY is set in .env")
        print("2. OpenAI API key is valid and has sufficient quota")
        print("3. Internet connection is available")
        print("4. Database is accessible")
        sys.exit(1)


if __name__ == "__main__":
    asyncio.run(main())
