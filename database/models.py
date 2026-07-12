"""
Database models.

These dataclasses represent records stored in the SQLite database.
"""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(slots=True, frozen=True)
class ProcessedEmail:
    """
    Represents a processed email stored in the database.
    """

    id: int | None

    message_id: str
    uid: str

    account_email: str

    sender_email: str

    subject: str

    received_at: str

    processed_at: str | None

    processing_status: str = "NEW"