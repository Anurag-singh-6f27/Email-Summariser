from __future__ import annotations

from database.connection import DatabaseManager
from database.models import ProcessedEmail
from mail.models import EmailData
from utils.logger import get_logger

logger = get_logger()


class ProcessedEmailRepository:
    """
    Repository for processed email records.
    """

    def __init__(self, database: DatabaseManager) -> None:
        self._database = database
        self._connection = database.get_connection()

    def initialize_database(self) -> None:
        """
        Initialize database schema.
        """
        self._database.initialize_database()

    def is_processed(self, message_id: str) -> bool:
        """
        Check whether an email has already been processed.
        """

        logger.info("Checking duplicate: {}", message_id)

        cursor = self._connection.execute(
            """
            SELECT 1
            FROM processed_emails
            WHERE message_id = ?
            LIMIT 1
            """,
            (message_id,),
        )

        return cursor.fetchone() is not None

    def save_processed_email(self, email: EmailData) -> None:
        """
        Save a processed email.
        """

        logger.info("Saving email: {}", email.subject)

        try:

            self._connection.execute(
                """
                INSERT INTO processed_emails
                (
                    message_id,
                    uid,
                    account_email,
                    sender_email,
                    subject,
                    received_at,
                    processing_status
                )
                VALUES
                (?, ?, ?, ?, ?, ?, ?)
                """,
                (
                    email.message_id,
                    email.uid,
                    email.account_email,
                    email.sender_email,
                    email.subject,
                    email.received_at.isoformat(),
                    "NEW",
                ),
            )

            self._connection.commit()

            logger.info("Email saved.")

        except Exception:

            logger.exception(
                "Failed to save email {}",
                email.message_id,
            )

            raise

    def count_processed(self) -> int:
        """
        Return total processed emails.
        """

        cursor = self._connection.execute(
            """
            SELECT COUNT(*)
            FROM processed_emails
            """
        )

        return int(cursor.fetchone()[0])

    def get_all_processed(self) -> list[ProcessedEmail]:
        """
        Return every processed email.
        """

        cursor = self._connection.execute(
            """
            SELECT *
            FROM processed_emails
            ORDER BY processed_at DESC
            """
        )

        rows = cursor.fetchall()

        emails: list[ProcessedEmail] = []

        for row in rows:

            emails.append(
                ProcessedEmail(
                    id=row["id"],
                    message_id=row["message_id"],
                    uid=row["uid"],
                    account_email=row["account_email"],
                    sender_email=row["sender_email"],
                    subject=row["subject"],
                    received_at=row["received_at"],
                    processed_at=row["processed_at"],
                    processing_status=row["processing_status"],
                )
            )

        return emails

    def delete_processed(self, message_id: str) -> bool:
        """
        Delete a processed email.
        """

        cursor = self._connection.execute(
            """
            DELETE
            FROM processed_emails
            WHERE message_id = ?
            """,
            (message_id,),
        )

        self._connection.commit()

        deleted = cursor.rowcount > 0

        if deleted:
            logger.info(
                "Deleted {}",
                message_id,
            )

        return deleted

    def filter_new_emails(
        self,
        emails: list[EmailData],
    ) -> list[EmailData]:
        """
        Return only emails that have not been processed.
        
        This method only filters emails. Saving processed
        emails is handled by the pipeline after successful
        processing.
        """

        new_emails: list[EmailData] = []

        for email in emails:

            if self.is_processed(email.message_id):

                logger.info(
                    "Duplicate detected: {}",
                    email.subject,
                )

                continue

            logger.info(
                "New email detected: {}",
                email.subject,
            )

            new_emails.append(email)

        return new_emails
    
    def get_processed_page(
        self,
        page: int,
        page_size: int,
    ) -> list[ProcessedEmail]:
        """
        Return one page of processed emails.
        """

        offset = (page - 1) * page_size

        cursor = self._connection.execute(
            """
            SELECT *
            FROM processed_emails
            ORDER BY processed_at DESC
            LIMIT ?
            OFFSET ?
            """,
            (
                page_size,
                offset,
            ),
        )

        rows = cursor.fetchall()

        emails: list[ProcessedEmail] = []

        for row in rows:

            emails.append(
                ProcessedEmail(
                    id=row["id"],
                    message_id=row["message_id"],
                    uid=row["uid"],
                    account_email=row["account_email"],
                    sender_email=row["sender_email"],
                    subject=row["subject"],
                    received_at=row["received_at"],
                    processed_at=row["processed_at"],
                    processing_status=row["processing_status"],
                )
            )

        return emails
    def count_processed(self) -> int:
        """
        Return total number of processed emails.
        """

        cursor = self._connection.execute(
            """
            SELECT COUNT(*)
            FROM processed_emails
            """
        )

        return int(cursor.fetchone()[0])