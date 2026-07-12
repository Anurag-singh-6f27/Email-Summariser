"""
Data models used by the AI summarization engine.

These models define the standardized objects exchanged
between AI providers and the rest of the application.
"""

from __future__ import annotations

from dataclasses import dataclass, field


# ==========================================================
# Structured Summary Content
# ==========================================================

@dataclass(slots=True)
class SummaryContent:
    """
    Structured information extracted from an email.
    """

    concise_summary: str

    category: str

    priority: str

    action_required: bool

    action_items: list[str] = field(default_factory=list)

    important_dates: list[str] = field(default_factory=list)

    meetings: list[str] = field(default_factory=list)

    financial_items: list[str] = field(default_factory=list)

    important_links: list[str] = field(default_factory=list)

    people: list[str] = field(default_factory=list)

    organizations: list[str] = field(default_factory=list)

    notes: list[str] = field(default_factory=list)


# ==========================================================
# AI Execution Metadata
# ==========================================================

@dataclass(slots=True)
class SummaryMetadata:
    """
    Metadata about the AI request.
    """

    provider: str

    model: str

    processing_time_ms: float

    tokens_used: int | None

    success: bool

    error: str | None = None


# ==========================================================
# Final Result
# ==========================================================

@dataclass(slots=True)
class SummaryResult:
    """
    Complete result returned by an AI provider.
    """

    content: SummaryContent

    metadata: SummaryMetadata