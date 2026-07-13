"""
Structured response schema used by AI providers.

This module defines the response format that every AI provider
(Gemini, Grok, NVIDIA, future providers) must return.

The Google GenAI SDK can use these models directly for
structured JSON generation.
"""

from __future__ import annotations

from typing import Literal

from pydantic import BaseModel, Field


# ==========================================================
# Structured Response Schema
# ==========================================================


class SummarySchema(BaseModel):
    """
    Structured summary returned by the AI.
    """

    concise_summary: str = Field(
        description="A concise factual summary of the email."
    )

    category: Literal[
        "JOB",
        "INTERVIEW",
        "SERVICE",
        "GITHUB",
        "BANK",
        "FINANCE",
        "PAYMENT",
        "SHOPPING",
        "ORDER",
        "SUBSCRIPTION",
        "BILL",
        "INVOICE",
        "TRAVEL",
        "MEETING",
        "CALENDAR",
        "COURSE",
        "EDUCATION",
        "SECURITY",
        "OTP",
        "SOCIAL",
        "NEWSLETTER",
        "PROMOTION",
        "HEALTH",
        "GOVERNMENT",
        "EVENT",
        "PERSONAL",
        "UNKNOWN",
    ]

    priority: Literal[
        "LOW",
        "MEDIUM",
        "HIGH",
        "CRITICAL",
    ]

    action_required: bool

    action_items: list[str] = Field(default_factory=list)

    important_dates: list[str] = Field(default_factory=list)

    meetings: list[str] = Field(default_factory=list)

    financial_items: list[str] = Field(default_factory=list)

    important_links: list[str] = Field(default_factory=list)

    people: list[str] = Field(default_factory=list)

    organizations: list[str] = Field(default_factory=list)

    notes: list[str] = Field(default_factory=list)