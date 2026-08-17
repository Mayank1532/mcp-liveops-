from __future__ import annotations

import pytest

from mcp_liveops.mcp import (
    McpClientAdapter,
    McpEvidenceTools,
    create_integrated_server,
)


def test_web_evidence_tool_uses_acquisition_layer() -> None:
    service = McpEvidenceTools()

    result = service.web_source(
        title="Example article",
        content="Important evidence content.",
        source_name="Example News",
        source_uri="https://example.com/article",
    )

    assert result.success is True
    assert result.output == "Important evidence content."
    assert result.error is None


def test_external_api_tool_uses_acquisition_layer() -> None:
    service = McpEvidenceTools()

    result = service.external_api(
        provider="NewsAPI",
        title="Example news",
        content="External evidence content.",
        source_name="Example News",
        endpoint="https://example.com/v1/articles",
    )

    assert result.success is True
    assert result.output == "External evidence content."
    assert result.error is None


def test_web_evidence_rejects_invalid_source() -> None:
    service = McpEvidenceTools()

    result = service.web_source(
        title="",
        content="Content",
        source_name="Example",
        source_uri="https://example.com",
    )

    assert result.success is False
    assert result.error is not None


@pytest.mark.anyio
async def test_integrated_mcp_discovers_evidence_tools() -> None:
    client = McpClientAdapter()

    tools = await client.discover_tools(
        create_integrated_server(),
    )

    assert tools == [
        "external_api_evidence",
        "live_weather",
        "web_evidence",
    ]


@pytest.mark.anyio
async def test_integrated_mcp_invokes_web_evidence() -> None:
    client = McpClientAdapter()

    result = await client.invoke(
        create_integrated_server(),
        "web_evidence",
        {
            "title": "Example",
            "content": "Normalized web evidence.",
            "source_name": "Example News",
            "source_uri": "https://example.com/article",
        },
    )

    assert result.success is True
    assert result.output == "Normalized web evidence."


@pytest.mark.anyio
async def test_integrated_mcp_invokes_external_api_evidence() -> None:
    client = McpClientAdapter()

    result = await client.invoke(
        create_integrated_server(),
        "external_api_evidence",
        {
            "provider": "NewsAPI",
            "title": "Example",
            "content": "Normalized API evidence.",
            "source_name": "Example News",
            "endpoint": "https://example.com/v1/articles",
        },
    )

    assert result.success is True
    assert result.output == "Normalized API evidence."


@pytest.mark.anyio
async def test_integrated_mcp_rejects_invalid_web_input() -> None:
    client = McpClientAdapter()

    result = await client.invoke(
        create_integrated_server(),
        "web_evidence",
        {
            "title": "",
            "content": "Content",
            "source_name": "Example",
            "source_uri": "https://example.com",
        },
    )

    assert result.success is False
    assert result.error is not None


@pytest.mark.anyio
async def test_integrated_mcp_unknown_tool_fails() -> None:
    client = McpClientAdapter()

    result = await client.invoke(
        create_integrated_server(),
        "unknown_evidence_tool",
    )

    assert result.success is False
    assert result.error is not None
