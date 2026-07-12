"""
Data models for email processing.

This module defines the standardized email object used
throughout the application.
"""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime


@dataclass(slots=True, frozen=True)
class EmailData:
    """
    Represents a parsed email.

    This object is passed between the reader,
    parser, AI summarizer, database, and Telegram modules.
    """

    uid: str
    message_id: str

    account_email: str

    sender_name: str
    sender_email: str
    recipient_email: str

    subject: str
    body: str

    received_at: datetime

    is_html: bool