"""MCP Server initialization with Official SDK

This module sets up the Model Context Protocol server and registers all task management tools.
"""

from typing import Any
import logging
from mcp.tools import add_task

logger = logging.getLogger(__name__)


class MCPServer:
    """Manages MCP server and tool registration"""

    def __init__(self):
        """Initialize MCP server"""
        self.tools: dict[str, Any] = {}
        logger.info("MCP Server initialized")

    def register_tool(self, name: str, tool: Any) -> None:
        """Register an MCP tool"""
        self.tools[name] = tool
        logger.info(f"Tool registered: {name}")

    def get_tools(self) -> dict[str, Any]:
        """Get all registered tools"""
        return self.tools


# Global MCP server instance
mcp_server = MCPServer()


def initialize_mcp_server() -> MCPServer:
    """Initialize and return MCP server with all tools

    Returns:
        MCPServer: Configured MCP server instance
    """
    logger.info("Initializing MCP server with all tools")

    # Register task management tools
    mcp_server.register_tool("add_task", add_task)

    logger.info(f"Registered tools: {list(mcp_server.get_tools().keys())}")

    return mcp_server
