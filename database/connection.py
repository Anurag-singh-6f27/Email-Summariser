"""
SQLite database connection manager.

Responsible for:
- Creating the SQLite database
- Creating tables
- Creating indexes
- Providing database connections
"""

from __future__ import annotations

import sqlite3
from pathlib import Path

from utils.logger import get_logger

logger = get_logger()


DATABASE_DIRECTORY = Path("data")
DATABASE_PATH = DATABASE_DIRECTORY / "emails.db"


class DatabaseManager:
    """
    Manages the SQLite database connection.
    """

    def __init__(self) -> None:
        DATABASE_DIRECTORY.mkdir(parents=True, exist_ok=True)

        self.connection = sqlite3.connect(DATABASE_PATH,
                                        check_same_thread=False,
                                        )

        self.connection.row_factory = sqlite3.Row

        logger.info("Database connection opened.")

    def initialize_database(self) -> None:
        """
        Create tables and indexes if they do not exist.
        """

        cursor = self.connection.cursor()

        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS processed_emails (

                id INTEGER PRIMARY KEY AUTOINCREMENT,

                message_id TEXT UNIQUE NOT NULL,

                uid TEXT NOT NULL,

                account_email TEXT NOT NULL,

                sender_email TEXT,

                subject TEXT,

                received_at TEXT,

                processed_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

                processing_status TEXT DEFAULT 'NEW'
            )
            """
        )

        cursor.execute(
            """
            CREATE INDEX IF NOT EXISTS idx_message_id
            ON processed_emails(message_id)
            """
        )

        cursor.execute(
            """
            CREATE INDEX IF NOT EXISTS idx_uid_account
            ON processed_emails(uid, account_email)
            """
        )

        self.connection.commit()

        logger.info("Database initialized successfully.")

    def get_connection(self) -> sqlite3.Connection:
        """
        Return the active SQLite connection.
        """

        return self.connection

    def close(self) -> None:
        """
        Close the SQLite connection.
        """

        self.connection.close()

        logger.info("Database connection closed.")