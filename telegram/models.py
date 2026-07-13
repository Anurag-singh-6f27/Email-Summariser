"""
Data models used by the Telegram notification layer.

These models represent messages that will be sent through
the Telegram Bot API.
"""

from __future__ import annotations

from dataclasses import dataclass


# ==========================================================
# Telegram Message
# ==========================================================

@dataclass(slots=True, frozen=True)
class TelegramMessage:
    """
    Represents a Telegram message ready to be sent.

    Attributes:
        text:
            Fully formatted Telegram message.

        parse_mode:
            Telegram parse mode.
            Usually "MarkdownV2" or "HTML".

        disable_web_page_preview:
            Whether Telegram should suppress
            URL previews.
    """

    text: str

    parse_mode: str = "MarkdownV2"

    disable_web_page_preview: bool = True