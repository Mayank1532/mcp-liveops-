"""Integrated NEXUS-SHIELD MCP server."""

from __future__ import annotations

from typing import Any

from mcp.server import MCPServer

from nexus_shield.mcp.evidence_tools import register_evidence_tools
from nexus_shield.mcp.live_weather import register_live_weather_tool


def create_integrated_server() -> MCPServer[Any]:
    """Create an MCP server with evidence acquisition tools."""

    server = MCPServer(
        "nexus-shield-evidence",
        version="0.1.0",
    )

    evidence = register_evidence_tools(server)
    register_live_weather_tool(server, evidence)

    return server
