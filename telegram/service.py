"""
Telegram notification service.

Coordinates formatting and delivery of Telegram
notifications.
"""

from __future__ import annotations

from config import TelegramConfig
from mail.models import EmailData

from ai.models import SummaryResult

from telegram.client import TelegramClient
from telegram.formatter import TelegramFormatter
from telegram.models import TelegramMessage

from utils.logger import get_logger

logger = get_logger()


class TelegramService:
    """
    Public interface for Telegram notifications.
    """

    def __init__(
        self,
        config: TelegramConfig,
    ) -> None:
        """
        Initialize the Telegram service.

        Args:
            config:
                Telegram configuration.
        """

        self._formatter = TelegramFormatter()

        self._client = TelegramClient(
            config
        )

    def send_email_summary(
        self,
        email: EmailData,
        summary: SummaryResult,
    ) -> bool:
        """
        Format and send an email summary.

        Args:
            email:
                Parsed email.

            summary:
                AI generated summary.

        Returns:
            True if the notification was delivered.
        """

        logger.info(
            "Preparing Telegram notification for '{}'.",
            email.subject,
        )

        message = self._formatter.format(
            email=email,
            summary=summary,
        )

        delivered = self._client.send_message(
            message
        )

        if delivered:

            logger.info(
                "Telegram notification sent successfully."
            )

        return delivered

    def send_message(
        self,
        message: TelegramMessage,
    ) -> bool:
        """
        Send a preformatted Telegram message.

        Args:
            message:
                TelegramMessage instance.

        Returns:
            True if successfully delivered.
        """

        logger.info(
            "Sending preformatted Telegram message."
        )

        return self._client.send_message(
            message
        )