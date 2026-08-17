"""MCP integration package."""

from mcp_liveops.mcp.client import McpClientAdapter
from mcp_liveops.mcp.coingecko_tools import (
    McpCoinGeckoTools,
    register_coingecko_tools,
)
from mcp_liveops.mcp.evidence_tools import (
    McpEvidenceTools,
    register_evidence_tools,
)
from mcp_liveops.mcp.integration_server import create_integrated_server
from mcp_liveops.mcp.models import (
    ToolExecutionResult,
    ToolMetadata,
)
from mcp_liveops.mcp.registry import ToolRegistry
from mcp_liveops.mcp.server import get_mcp_server

__all__ = [
    "McpClientAdapter",
    "McpCoinGeckoTools",
    "McpEvidenceTools",
    "ToolExecutionResult",
    "ToolMetadata",
    "ToolRegistry",
    "create_integrated_server",
    "get_mcp_server",
    "register_coingecko_tools",
    "register_evidence_tools",
]
