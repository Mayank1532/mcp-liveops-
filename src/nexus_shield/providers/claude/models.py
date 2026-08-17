"""Claude gateway domain models."""

from dataclasses import dataclass


@dataclass(frozen=True)
class ClaudeRequest:
    """Input to the Claude gateway."""

    prompt: str
    system_prompt: str | None = None
    max_tokens: int = 1024
    temperature: float = 0.0


@dataclass(frozen=True)
class ClaudeUsage:
    """Token usage returned by the model."""

    input_tokens: int
    output_tokens: int


@dataclass(frozen=True)
class ClaudeResponse:
    """Normalized Claude gateway response."""

    text: str
    model: str
    usage: ClaudeUsage
    latency_ms: float
    stop_reason: str | None
