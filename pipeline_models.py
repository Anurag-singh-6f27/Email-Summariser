"""
Models used by the application processing pipeline.
"""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime


@dataclass(slots=True)
class PipelineStatistics:
    """
    Statistics generated after a complete pipeline execution.

    Attributes:
        start_time:
            Time when pipeline execution started.

        end_time:
            Time when pipeline execution finished.

        duration_seconds:
            Total execution time in seconds.

        accounts_processed:
            Number of email accounts processed.

        emails_fetched:
            Total unread emails fetched.

        duplicates_skipped:
            Emails skipped because they were already processed.

        summaries_generated:
            Number of AI summaries successfully generated.

        telegram_messages_sent:
            Number of Telegram notifications successfully delivered.

        errors:
            Number of processing errors encountered.

        success:
            Whether the pipeline completed successfully.
    """

    start_time: datetime

    end_time: datetime

    duration_seconds: float

    accounts_processed: int

    emails_fetched: int

    duplicates_skipped: int

    summaries_generated: int

    telegram_messages_sent: int

    errors: int

    success: bool