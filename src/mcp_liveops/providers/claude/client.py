"""Claude provider abstraction."""

from __future__ import annotations

import time
from typing import Protocol, cast

from anthropic import Anthropic
from anthropic.types import TextBlock

from mcp_liveops.config.settings import Settings
from mcp_liveops.providers.claude.models import (
    ClaudeRequest,
    ClaudeResponse,
    ClaudeUsage,
)


class ClaudeClient(Protocol):
    """Protocol implemented by Claude-compatible clients."""

    def create_message(self, request: ClaudeRequest) -> ClaudeResponse:
        """Generate a response from the model."""


class AnthropicClaudeClient:
    """Claude client backed by the Anthropic API."""

    def __init__(self, settings: Settings) -> None:
        self._settings = settings

        api_key = settings.anthropic_api_key.get_secret_value()

        if not api_key:
            raise ValueError(
                "ANTHROPIC_API_KEY is not configured. "
                "Set it in the .env file before using Claude."
            )

        self._client = Anthropic(
            api_key=api_key,
            timeout=settings.claude_timeout_seconds,
        )

    def create_message(self, request: ClaudeRequest) -> ClaudeResponse:
        """Send a request to Claude and normalize the response."""

        if not request.prompt.strip():
            raise ValueError("Claude prompt cannot be empty.")

        started = time.perf_counter()

        message = self._client.messages.create(
            model=self._settings.claude_model,
            max_tokens=request.max_tokens,
            temperature=request.temperature,
            system=request.system_prompt or "",
            messages=[
                {
                    "role": "user",
                    "content": request.prompt,
                }
            ],
        )

        latency_ms = (time.perf_counter() - started) * 1000

        text_parts: list[str] = []

        for block in message.content:
            if getattr(block, "type", None) == "text":
                text_block = cast(TextBlock, block)
                text_parts.append(text_block.text)

        text = "".join(text_parts).strip()

        usage = ClaudeUsage(
            input_tokens=message.usage.input_tokens,
            output_tokens=message.usage.output_tokens,
        )

        return ClaudeResponse(
            text=text,
            model=message.model,
            usage=usage,
            latency_ms=latency_ms,
            stop_reason=message.stop_reason,
        )

