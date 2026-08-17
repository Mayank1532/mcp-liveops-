"""MCP integration package."""

from nexus_shield.mcp.client import McpClientAdapter
from nexus_shield.mcp.evidence_tools import (
    McpEvidenceTools,
    register_evidence_tools,
)
from nexus_shield.mcp.integration_server import create_integrated_server
from nexus_shield.mcp.models import (
    ToolExecutionResult,
    ToolMetadata,
)
from nexus_shield.mcp.registry import ToolRegistry
from nexus_shield.mcp.server import get_mcp_server

__all__ = [
    "McpClientAdapter",
    "McpEvidenceTools",
    "ToolExecutionResult",
    "ToolMetadata",
    "ToolRegistry",
    "create_integrated_server",
    "get_mcp_server",
    "register_evidence_tools",
]