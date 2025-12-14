# OpenAI Agents SDK Reference Documentation

**Last Updated**: December 14, 2025
**Source**: Official OpenAI Documentation

## Overview

The OpenAI Agents SDK is a lightweight, powerful framework for building multi-agent workflows. It enables developers to build agentic applications where models can use additional context and tools, hand off to other specialized agents, stream partial results, and maintain full traces of execution.

## Official Resources

- **Platform Documentation**: https://platform.openai.com/docs/guides/agents-sdk
- **Python SDK Docs**: https://openai.github.io/openai-agents-python/
- **GitHub Repository**: https://github.com/openai/openai-agents-python
- **API Reference**: https://platform.openai.com/docs/api-reference/agents
- **Blog Post**: https://openai.com/index/new-tools-for-building-agents/

## Core Primitives

The Agents SDK is built on a small set of foundational primitives:

### 1. Agents
- LLMs equipped with instructions and tools
- Autonomously select and invoke appropriate tools
- Can delegate to other agents (handoffs)
- Maintain conversation context

### 2. Handoffs
- Allow agents to delegate to other specialized agents
- Enable multi-agent workflows
- Route requests based on task type

### 3. Guardrails
- Enable validation of agent inputs
- Validate agent outputs before returning to user
- Ensure safety and compliance

### 4. Sessions
- Automatically maintain conversation history
- Track across agent runs
- Enable stateless request handling (state in database)

## Architecture Pattern

```
User Request
    ↓
Agent (with tools + instructions)
    ↓
Tool Invocation (MCP Tools)
    ↓
External Service (Database, API, etc.)
    ↓
Response Stream
    ↓
User
```

## API Compatibility

The Agents SDK works with:
- **OpenAI Models**: GPT-4, GPT-4o, and other OpenAI models
- **Chat Completions API**: Standard OpenAI API endpoint
- **Third-party Models**: Compatible with any provider offering Chat Completions style API

## Tool Integration

### Defining Tools

Tools are defined with:
- **Name**: Unique identifier
- **Description**: Natural language description
- **Parameters**: Input schema (JSON Schema format)
- **Execution Logic**: Handler function

### Tool Execution

```python
# Agent automatically selects and invokes tools
agent = Agent(
    model="gpt-4o",
    tools=[add_task_tool, list_tasks_tool, complete_task_tool]
)

# Agent invokes tools based on user request
response = agent.run(user_message)
```

## Key Features for Phase 3

- ✅ Tool invocation with automatic selection
- ✅ Multi-tool execution in single turn
- ✅ Streaming responses
- ✅ Error handling and retries
- ✅ Full execution trace
- ✅ Context preservation across turns

## Integration with MCP

The Agents SDK can use MCP Tools directly:
- Define MCP tools
- Pass to Agent constructor
- Agent selects and invokes tools automatically
- Enables declarative tool definition

## Authentication

```python
from openai import OpenAI

client = OpenAI(api_key="sk-...")

# Agent initialized with authenticated client
agent = Agent(
    client=client,
    model="gpt-4o",
    tools=[...]
)
```

## Best Practices for Phase 3

1. **Tool Design**: Each tool should be single-purpose and stateless
2. **Error Handling**: Tools should gracefully handle errors
3. **User Isolation**: Tools validate user_id from context
4. **Streaming**: Enable streaming for better UX
5. **Tracing**: Maintain full execution trace for debugging
6. **Testing**: Test tool behavior independently

## Streaming Example

```python
# Streaming response from agent
for chunk in agent.run(message, stream=True):
    print(chunk.text)
```

## Advanced Features

- **Handoffs**: Route to specialized agents
- **Guardrails**: Validate inputs/outputs
- **Context Windows**: Manage conversation history
- **Multi-turn**: Maintain state across requests

## For Phase 3 Implementation

The Agents SDK will be used to:
1. Initialize agent with MCP tools
2. Process user message
3. Agent selects appropriate MCP tool(s)
4. Stream response back to frontend
5. ChatKit displays streamed messages and tool invocations

## Version Information

- Minimum Version: Latest stable
- Python Version: 3.13+
- FastAPI Compatibility: Yes
- Tested with: OpenAI API v1

## Related Documentation

- OpenAI API Documentation: https://platform.openai.com/docs/api-reference
- Chat Completions: https://platform.openai.com/docs/guides/chat-completions
- Function Calling: https://platform.openai.com/docs/guides/function-calling
