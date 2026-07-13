"""
Custom exceptions used by the Telegram notification layer.
"""

from __future__ import annotations


class TelegramError(Exception):
    """
    Base exception for all Telegram-related errors.
    """

    pass


class InvalidBotTokenError(TelegramError):
    """
    Raised when the configured bot token
    is invalid.
    """

    pass


class InvalidChatIDError(TelegramError):
    """
    Raised when the configured chat ID
    cannot be found.
    """

    pass


class TelegramRateLimitError(TelegramError):
    """
    Raised when Telegram rate limits
    the application.
    """

    pass


class TelegramTimeoutError(TelegramError):
    """
    Raised when a Telegram request
    times out.
    """

    pass


class TelegramAPIError(TelegramError):
    """
    Raised when Telegram returns an
    unexpected API error.
    """

    pass


class MessageTooLongError(TelegramError):
    """
    Raised when a message exceeds
    Telegram's maximum length.
    """

    pass


class MarkdownFormattingError(TelegramError):
    """
    Raised when Telegram rejects
    Markdown formatting.
    """

    pass