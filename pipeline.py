"""
Application processing pipeline.

Coordinates the complete workflow for reading emails,
generating AI summaries, sending Telegram notifications,
and persisting processed emails.
"""

from __future__ import annotations

from datetime import datetime
from mail.models import EmailData
from config import AppConfig
from database.connection import DatabaseManager
from database.repository import ProcessedEmailRepository
from mail.reader import EmailReader
from ai.service import AIService
from telegram.service import TelegramService

from pipeline_models import PipelineStatistics

from utils.logger import get_logger

logger = get_logger()


class Pipeline:
    """
    Coordinates the complete email processing pipeline.
    """

    def __init__(
        self,
        config: AppConfig,
    ) -> None:
        """
        Initialize the processing pipeline.

        Args:
            config:
                Application configuration.
        """

        self._config = config

        self._database = DatabaseManager()

        self._repository = ProcessedEmailRepository(
            self._database
        )

        self._reader = EmailReader(
            config
        )

        self._ai_service = AIService(
            config.ai
        )

        self._telegram_service = TelegramService(
            config.telegram
        )

    def run(
        self,
    ) -> PipelineStatistics:

        logger.info(
            "Pipeline execution started."
        )

        start_time = datetime.now()

        self._repository.initialize_database()

        emails = self._reader.fetch_all_unread()

        emails_fetched = len(emails)

        if not emails:

            logger.info(
                "No unread emails found within the last {} days.",
                self._config.email_retention_days,
            )

            return self._build_statistics(
                start_time=start_time,
                end_time=datetime.now(),
                emails_fetched=0,
                duplicates_skipped=0,
                summaries_generated=0,
                telegram_messages_sent=0,
                errors=0,
            )

        new_emails = self._repository.filter_new_emails(
            emails
        )

        logger.info(
            "New emails to process: {}",
            len(new_emails),
        )

        duplicates_skipped = (
            emails_fetched - len(new_emails)
        )

        if not new_emails:

            logger.info(
                "All fetched emails were already processed. Skipping pipeline execution."
            )

            return self._build_statistics(
                start_time=start_time,
                end_time=datetime.now(),
                emails_fetched=emails_fetched,
                duplicates_skipped=duplicates_skipped,
                summaries_generated=0,
                telegram_messages_sent=0,
                errors=0,
            )

        summaries_generated = 0

        telegram_messages_sent = 0

        errors = 0

        for email in new_emails:

            logger.info(
                "Starting email: {}",
                email.subject,
            )

            try:

                delivered = self._process_email(
                    email
                )

                summaries_generated += 1

                if delivered:
                    telegram_messages_sent += 1

            except Exception:

                errors += 1

                logger.exception(
                    "Failed processing '{}'.",
                    email.subject,
                )

        end_time = datetime.now()

        return self._build_statistics(
            start_time=start_time,
            end_time=end_time,
            emails_fetched=emails_fetched,
            duplicates_skipped=duplicates_skipped,
            summaries_generated=summaries_generated,
            telegram_messages_sent=telegram_messages_sent,
            errors=errors,
        )
    

    def _process_email(
        self,
        email:EmailData,
    ) -> bool:
        """
        Process a single email.

        Args:
            email:
                Parsed email.

        Returns:
            True if the Telegram notification was
            delivered successfully.
        """

        logger.info(
            "Processing '{}'.",
            email.subject,
        )

        summary = self._ai_service.summarize(
            email
        )

        delivered = (
            self._telegram_service.send_email_summary(
                email,
                summary,
            )
        )

        if delivered:

            self._repository.save_processed_email(
                email
            )

            logger.info(
                "Email '{}' processed successfully.",
                email.subject,
            )

        else:

            logger.warning(
                "Telegram delivery failed for '{}'. Email will be retried later.",
                email.subject,
            )

        return delivered

    def _build_statistics(
        self,
        start_time: datetime,
        end_time: datetime,
        emails_fetched: int,
        duplicates_skipped: int,
        summaries_generated: int,
        telegram_messages_sent: int,
        errors: int,
    ) -> PipelineStatistics:
        """
        Build execution statistics.

        Args:
            start_time:
                Pipeline start time.

            end_time:
                Pipeline end time.

            emails_fetched:
                Total unread emails fetched.

            duplicates_skipped:
                Duplicate emails skipped.

            summaries_generated:
                Successfully generated summaries.

            telegram_messages_sent:
                Successfully delivered notifications.

            errors:
                Total processing errors.

        Returns:
            PipelineStatistics
        """

        duration = (
            end_time - start_time
        ).total_seconds()

        statistics = PipelineStatistics(
            start_time=start_time,
            end_time=end_time,
            duration_seconds=duration,
            accounts_processed=len(
                self._config.email_accounts
            ),
            emails_fetched=emails_fetched,
            duplicates_skipped=duplicates_skipped,
            summaries_generated=summaries_generated,
            telegram_messages_sent=telegram_messages_sent,
            errors=errors,
            success=(errors == 0),
        )

        logger.info(
            "Pipeline completed in {:.2f} seconds.",
            statistics.duration_seconds,
        )

        logger.info(
            "Accounts processed: {}",
            statistics.accounts_processed,
        )

        logger.info(
            "Emails fetched: {}",
            statistics.emails_fetched,
        )

        logger.info(
            "Duplicates skipped: {}",
            statistics.duplicates_skipped,
        )

        logger.info(
            "Summaries generated: {}",
            statistics.summaries_generated,
        )

        logger.info(
            "Telegram notifications sent: {}",
            statistics.telegram_messages_sent,
        )

        logger.info(
            "Errors: {}",
            statistics.errors,
        )

        return statistics

    def close(
        self,
    ) -> None:
        """
        Release pipeline resources.
        """

        logger.info(
            "Closing pipeline."
        )

        self._database.close()