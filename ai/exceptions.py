"""
Custom exceptions used by the AI summarization layer.

Every AI provider (Gemini, Grok, future providers)
should raise these exceptions instead of generic
RuntimeError or Exception.
"""

from __future__ import annotations


class AIServiceError(Exception):
    """
    Base exception for all AI-related errors.
    """

    pass


class InvalidAPIKeyError(AIServiceError):
    """
    Raised when the configured API key is invalid.
    """

    pass


class RateLimitError(AIServiceError):
    """
    Raised when the provider rate limit is exceeded.
    """

    pass


class ModelUnavailableError(AIServiceError):
    """
    Raised when the selected AI model is unavailable.
    """

    pass


class NetworkTimeoutError(AIServiceError):
    """
    Raised when an AI request exceeds the timeout.
    """

    pass


class InvalidResponseError(AIServiceError):
    """
    Raised when the AI returns an invalid or
    unexpected response.
    """

    pass


class EmptySummaryError(AIServiceError):
    """
    Raised when the AI returns an empty summary.
    """

    pass


class JSONParseError(AIServiceError):
    """
    Raised when the AI response cannot be parsed
    into the expected JSON structure.
    """

    pass


class ProviderNotConfiguredError(AIServiceError):
    """
    Raised when the requested AI provider
    has not been configured.
    """

    pass