# Model Context Protocol (MCP) Reference Documentation

**Last Updated**: December 14, 2025
**MCP Specification Version**: 2025-06-18
**Source**: Official Model Context Protocol Documentation

## Overview

Model Context Protocol (MCP) is an open protocol that enables seamless integration between LLM applications and external data sources and tools. It provides a standardized way for AI systems to interact with resources, prompts, and tools.

## Official Resources

- **Specification**: https://modelcontextprotocol.io/specification/2025-06-18
- **GitHub Organization**: https://github.com/modelcontextprotocol
- **Python SDK**: https://github.com/modelcontextprotocol/python-sdk
- **Main Documentation**: https://modelcontextprotocol.io
- **Anthropic Announcement**: https://www.anthropic.com/news/model-context-protocol

## What is MCP?

MCP is an open protocol that standardizes how applications can:
- Expose resources to LLMs
- Define available tools/functions
- Provide prompts and context
- Communicate between clients and servers

## Official SDKs Available

### Python SDK (Primary for Phase 3)
```bash
pip install mcp
```

**Repository**: https://github.com/modelcontextprotocol/python-sdk

**Features**:
- Full MCP specification implementation
- Build MCP servers (expose resources, prompts, tools)
- Build MCP clients (connect to MCP servers)
- Standard transports: stdio, SSE, HTTP

### Other Official SDKs
- **TypeScript SDK**: Reference implementation, feature-complete
- **C# SDK**: Maintained in collaboration with Microsoft
- **Go SDK**: Maintained in collaboration with Google
- **Java SDK**: Community implementation

## MCP Architecture

```
MCP Client                      MCP Server
(LLM Application)              (Data/Tool Provider)
    |                                |
    |------- Transport Layer --------|
    |                                |
    Request (Tool/Resource)          |
    |------- JSON-RPC 2.0 ---------->|
    |                                |
    |                   Process Request
    |                   Access Resource
    |                   Invoke Tool
    |                                |
    |<------ JSON-RPC 2.0 ------Response
```

## Key Protocol Features

### 1. Tools
- Structured tool definitions
- JSON Schema for parameters
- Tool invocation with automatic execution

### 2. Resources
- Expose data sources to LLMs
- Read-only or read-write
- Support caching

### 3. Prompts
- Pre-defined prompt templates
- Parameterizable
- Reusable across agents

### 4. Transports
- **Stdio**: Process communication
- **SSE**: Server-Sent Events
- **HTTP**: Direct HTTP requests

## MCP Tool Definition

A typical MCP tool has:

```python
{
    "name": "add_task",
    "description": "Create a new task",
    "inputSchema": {
        "type": "object",
        "properties": {
            "user_id": {"type": "string"},
            "title": {"type": "string"},
            "description": {"type": "string"}
        },
        "required": ["user_id", "title"]
    }
}
```

## Building an MCP Server (Python)

```python
from mcp.server.fastmcp import FastMCP

mcp = FastMCP("task-server")

@mcp.tool()
def add_task(user_id: str, title: str, description: str = "") -> dict:
    """Create a new task."""
    # Implementation
    return {"task_id": 1, "title": title}

# Serve via stdio
if __name__ == "__main__":
    mcp.run()
```

## Building an MCP Client (Python)

```python
import asyncio
from mcp.client.session import ClientSession
from mcp.client.stdio import StdioClientTransport

async def main():
    transport = StdioClientTransport(command="python", args=["server.py"])
    async with ClientSession(transport) as session:
        # Call tool
        result = await session.call_tool("add_task", {
            "user_id": "user1",
            "title": "Buy groceries"
        })
```

## Protocol Message Types

### 1. Initialize
- Client initiates connection
- Negotiates capabilities
- Exchanges version info

### 2. Tool Calls
- Client requests tool execution
- Server processes and returns result
- Error handling with standard codes

### 3. Resource Access
- Client reads/writes resources
- Server manages access control
- Supports caching hints

### 4. Prompts
- Client requests prompt template
- Server returns parameterized prompt
- Client fills parameters

## Security & Best Practices

### 1. Authentication
- Implement authentication before tool access
- Validate user_id for multi-user systems
- Use JWT tokens from headers

### 2. Authorization
- Enforce resource ownership
- Limit tool access per user
- Log all tool invocations

### 3. Error Handling
- Return standard error codes
- Provide helpful error messages
- Never expose sensitive data in errors

### 4. Validation
- Validate all input parameters
- Use JSON Schema for contract enforcement
- Reject invalid requests

## MCP for Phase 3: Task Management

### Tools to Expose

1. **add_task**
   - Input: user_id, title, description
   - Output: task_id, title, status
   - Error: validation errors, user not found

2. **list_tasks**
   - Input: user_id, status (optional)
   - Output: array of tasks
   - Error: user not found

3. **complete_task**
   - Input: user_id, task_id
   - Output: task_id, status
   - Error: task not found, access denied

4. **delete_task**
   - Input: user_id, task_id
   - Output: task_id, status
   - Error: task not found, access denied

5. **update_task**
   - Input: user_id, task_id, title, description
   - Output: task_id, title, status
   - Error: validation errors, task not found

## Integration with OpenAI Agents SDK

The Agents SDK can use MCP tools:

```python
from openai.agents import Agent

agent = Agent(
    model="gpt-4o",
    mcp_server_url="http://localhost:3000",  # MCP server endpoint
    tools=["add_task", "list_tasks", "complete_task"]  # Available tools
)
```

## Stateless MCP Server Pattern (Phase 3)

```
Client Request
    ↓
MCP Server (Stateless)
    ├─ Extract user_id from JWT token
    ├─ Validate user authorization
    ├─ Execute tool
    └─ Query/Update database
    ↓
Database (State)
    ├─ Execute query
    ├─ Update data
    └─ Return result
    ↓
Server Response (Streamed)
    ↓
ChatKit Display
```

## HTTP Transport Example (Phase 3)

```python
# Backend exposes MCP tools via HTTP
@app.post("/mcp/tools/call")
async def call_mcp_tool(
    user_id: str = Depends(get_current_user),
    tool_name: str,
    parameters: dict
):
    # Validate user authorization
    # Execute tool with user context
    # Return result
    pass
```

## Recent 2025 Updates

In December 2025, Anthropic donated the MCP to the **Agentic AI Foundation (AAIF)**, a directed fund under the Linux Foundation, co-founded by:
- Anthropic
- Block
- OpenAI

With support from:
- Google
- Microsoft
- Amazon Web Services (AWS)
- Cloudflare
- Bloomberg

This ensures long-term vendor neutrality and cross-platform support.

## Advantages of MCP for Phase 3

1. **Standardized Interface**: Tools defined once, usable by any MCP client
2. **Vendor Neutral**: Works with OpenAI, Anthropic, or any LLM provider
3. **Composable**: Tools can be chained and composed
4. **Stateless**: Server holds no state (perfect for scalability)
5. **Type Safe**: JSON Schema enforces contracts
6. **Debuggable**: Full protocol trace available
7. **Testable**: Tools tested independently

## Testing MCP Tools

```python
# Unit test MCP tool
async def test_add_task():
    result = await add_task("user1", "Buy groceries", "Milk, eggs")
    assert result["task_id"] > 0
    assert result["title"] == "Buy groceries"

# Integration test with database
async def test_add_task_persists():
    result = await add_task("user1", "Test", "")
    # Verify in database
    db_task = db.query(Task).filter_by(id=result["task_id"]).first()
    assert db_task is not None
```

## Performance Considerations

- Tools should complete in < 2 seconds
- Use connection pooling for database
- Cache frequently accessed data
- Monitor tool latency
- Implement circuit breakers for external services

## Version Information

- Specification Version: 2025-06-18
- Python SDK: Latest from GitHub
- Compatibility: Python 3.13+
- FastAPI: Yes
- Async: Full async/await support

## For Phase 3 Implementation

The MCP protocol will be used to:
1. Define 5 task management tools
2. Expose tools via stateless MCP server
3. OpenAI Agents SDK calls MCP tools
4. Tools access database and enforce user isolation
5. Responses streamed back through ChatKit

## Related Documentation

- MCP Specification: https://modelcontextprotocol.io/specification/2025-06-18
- Python SDK Docs: https://github.com/modelcontextprotocol/python-sdk
- OpenAI Integration: https://openai.github.io/openai-agents-python/mcp/
- Examples: https://github.com/modelcontextprotocol/python-sdk/tree/main/examples
