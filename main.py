"""
Application entry point for the Personal AI Email Summarizer.

Responsibilities:
- Initialize logging
- Load configuration
- Initialize database
- Read unread emails
- Filter duplicates
- Display only new emails
"""

from __future__ import annotations

import sys

from config import load_config
from database.connection import DatabaseManager
from database.repository import ProcessedEmailRepository
from mail.reader import EmailReader
from utils.logger import get_logger, setup_logger


def main() -> None:
    """
    Main application entry point.
    """

    setup_logger()
    logger = get_logger()

    logger.info("=" * 60)
    logger.info("Starting Personal AI Email Summarizer")
    logger.info("=" * 60)

    database = None

    try:
        logger.info("Loading configuration...")

        config = load_config()

        logger.info(
            "Loaded {} configured email account(s).",
            len(config.email_accounts),
        )

        database = DatabaseManager()

        repository = ProcessedEmailRepository(database)

        repository.initialize_database()

        logger.info("Database initialized.")

        reader = EmailReader(config)

        logger.info("Reading inbox...")

        emails = reader.fetch_all_unread()

        logger.info(
            "Fetched {} unread email(s).",
            len(emails),
        )

        logger.info("Checking duplicates...")

        new_emails = repository.filter_new_emails(emails)

        duplicate_count = len(emails) - len(new_emails)

        logger.info(
            "{} new email(s).",
            len(new_emails),
        )

        logger.info(
            "{} duplicate email(s) skipped.",
            duplicate_count,
        )

        for index, email_data in enumerate(new_emails, start=1):

            logger.info("-" * 60)
            logger.info("Email {}", index)
            logger.info("From    : {}", email_data.sender_email)
            logger.info("Subject : {}", email_data.subject)
            logger.info("Date    : {}", email_data.received_at)
            logger.info(
                "Preview : {}",
                email_data.body[:150],
            )

        logger.info(
            "Total processed emails stored: {}",
            repository.count_processed(),
        )

        logger.info("=" * 60)
        logger.info("Application finished successfully.")
        logger.info("=" * 60)

    except Exception:
        logger.exception("Application terminated unexpectedly.")
        sys.exit(1)

    finally:
        if database is not None:
            database.close()


if __name__ == "__main__":
    main()