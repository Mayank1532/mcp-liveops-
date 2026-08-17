from types import SimpleNamespace
from unittest.mock import MagicMock

import pytest

from mcp_liveops.config import Settings
from mcp_liveops.providers.claude import (
    AnthropicClaudeClient,
    ClaudeRequest,
)


def test_settings_defaults() -> None:
    settings = Settings()

    assert settings.claude_model == "claude-sonnet-4-5"
    assert settings.claude_max_tokens == 1024
    assert settings.claude_temperature == 0.0
    assert settings.claude_timeout_seconds == 30.0


def test_missing_api_key_is_rejected() -> None:
    settings = Settings(anthropic_api_key="")

    with pytest.raises(ValueError, match="ANTHROPIC_API_KEY"):
        AnthropicClaudeClient(settings)


def test_empty_prompt_is_rejected() -> None:
    settings = Settings(anthropic_api_key="test-key")

    client = AnthropicClaudeClient(settings)

    client._client = MagicMock()

    with pytest.raises(ValueError, match="prompt cannot be empty"):
        client.create_message(
            ClaudeRequest(prompt="   ")
        )


def test_successful_response_is_normalized() -> None:
    settings = Settings(
        anthropic_api_key="test-key",
        claude_model="claude-test-model",
    )

    client = AnthropicClaudeClient(settings)

    fake_message = SimpleNamespace(
        content=[
            SimpleNamespace(
                type="text",
                text="Hello from Claude.",
            )
        ],
        model="claude-test-model",
        usage=SimpleNamespace(
            input_tokens=12,
            output_tokens=7,
        ),
        stop_reason="end_turn",
    )

    client._client = MagicMock()

    client._client.messages.create.return_value = fake_message

    response = client.create_message(
        ClaudeRequest(
            prompt="Say hello.",
            system_prompt="You are a test assistant.",
            max_tokens=100,
            temperature=0.0,
        )
    )

    assert response.text == "Hello from Claude."
    assert response.model == "claude-test-model"
    assert response.usage.input_tokens == 12
    assert response.usage.output_tokens == 7
    assert response.latency_ms >= 0
    assert response.stop_reason == "end_turn"

    client._client.messages.create.assert_called_once()


def test_request_parameters_are_forwarded() -> None:
    settings = Settings(
        anthropic_api_key="test-key",
        claude_model="claude-test-model",
    )

    client = AnthropicClaudeClient(settings)

    fake_message = SimpleNamespace(
        content=[
            SimpleNamespace(
                type="text",
                text="OK",
            )
        ],
        model="claude-test-model",
        usage=SimpleNamespace(
            input_tokens=1,
            output_tokens=1,
        ),
        stop_reason="end_turn",
    )

    client._client = MagicMock()
    client._client.messages.create.return_value = fake_message

    request = ClaudeRequest(
        prompt="Test prompt",
        system_prompt="Test system",
        max_tokens=200,
        temperature=0.0,
    )

    client.create_message(request)

    call = client._client.messages.create.call_args

    assert call.kwargs["model"] == "claude-test-model"
    assert call.kwargs["max_tokens"] == 200
    assert call.kwargs["temperature"] == 0.0
    assert call.kwargs["system"] == "Test system"
    assert call.kwargs["messages"] == [
        {
            "role": "user",
            "content": "Test prompt",
        }
    ]


def test_multiple_text_blocks_are_combined() -> None:
    settings = Settings(anthropic_api_key="test-key")

    client = AnthropicClaudeClient(settings)

    fake_message = SimpleNamespace(
        content=[
            SimpleNamespace(type="text", text="Part one. "),
            SimpleNamespace(type="text", text="Part two."),
        ],
        model="claude-test-model",
        usage=SimpleNamespace(
            input_tokens=5,
            output_tokens=5,
        ),
        stop_reason="end_turn",
    )

    client._client = MagicMock()
    client._client.messages.create.return_value = fake_message

    response = client.create_message(
        ClaudeRequest(prompt="Combine this.")
    )

    assert response.text == "Part one. Part two."


def test_non_text_blocks_are_ignored() -> None:
    settings = Settings(anthropic_api_key="test-key")

    client = AnthropicClaudeClient(settings)

    fake_message = SimpleNamespace(
        content=[
            SimpleNamespace(
                type="tool_use",
                id="tool_1",
            ),
            SimpleNamespace(
                type="text",
                text="Final text.",
            ),
        ],
        model="claude-test-model",
        usage=SimpleNamespace(
            input_tokens=5,
            output_tokens=5,
        ),
        stop_reason="end_turn",
    )

    client._client = MagicMock()
    client._client.messages.create.return_value = fake_message

    response = client.create_message(
        ClaudeRequest(prompt="Test mixed content.")
    )

    assert response.text == "Final text."

