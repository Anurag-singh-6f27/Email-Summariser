"""
Telegram Bot API client.

Responsible only for communicating with the Telegram Bot API.
"""

from __future__ import annotations

import requests

import time

from requests import ConnectionError

from config import TelegramConfig

from telegram.models import TelegramMessage
from telegram.exceptions import (
    InvalidBotTokenError,
    InvalidChatIDError,
    MarkdownFormattingError,
    MessageTooLongError,
    TelegramAPIError,
    TelegramRateLimitError,
    TelegramTimeoutError,
)

from utils.logger import get_logger

logger = get_logger()


class TelegramClient:
    """
    Telegram Bot API client.
    """

    DEFAULT_TIMEOUT = 15

    def __init__(
        self,
        config: TelegramConfig,
    ) -> None:

        self._config = config

        self._endpoint = (
            f"https://api.telegram.org/"
            f"bot{config.bot_token}/sendMessage"
        )

    def send_message(
        self,
        message: TelegramMessage,
    ) -> bool:
        """
        Send a Telegram message.

        Args:
            message:
                TelegramMessage to send.

        Returns:
            True if successfully delivered.

        Raises:
            InvalidBotTokenError
            InvalidChatIDError
            TelegramTimeoutError
            TelegramRateLimitError
            MessageTooLongError
            MarkdownFormattingError
            TelegramAPIError
        """

        logger.info(
            "Sending Telegram notification..."
        )

        if len(message.text) > 4096:

            raise MessageTooLongError(
                "Telegram message exceeds 4096 characters."
            )

        payload = {

            "chat_id": self._config.chat_id,

            "text": message.text,

            "parse_mode": message.parse_mode,

            "disable_web_page_preview":
                message.disable_web_page_preview,
        }

        response = None

        for attempt in range(
            1,
            self._config.retry_count + 1,
        ):

            try:

                logger.info(
                    "Telegram send attempt {}/{}.",
                    attempt,
                    self._config.retry_count,
                )

                response = requests.post(

                    self._endpoint,

                    json=payload,

                    timeout=self.DEFAULT_TIMEOUT,
                )

                if (
                    response.status_code != 429
                    and response.status_code < 500
                ):
                    break

                logger.warning(
                    "Telegram returned HTTP {} on attempt {}/{}.",
                    response.status_code,
                    attempt,
                    self._config.retry_count,
                )
                if attempt == self._config.retry_count:
                    logger.error(
                        "Telegram retry limit exceeded."
                    )
                    break

            except (
                requests.Timeout,
                ConnectionError,
            ) as exc:

                logger.warning(
                    "Telegram request failed on attempt {}/{}: {}",
                    attempt,
                    self._config.retry_count,
                    exc,
                )

                if attempt == self._config.retry_count:
                    logger.error(
                        "Telegram retry limit exceeded."
                    )

                    raise TelegramTimeoutError(
                        str(exc)
                    ) from exc

            except requests.RequestException as exc:

                logger.exception(
                    "Network error while contacting Telegram."
                )

                raise TelegramAPIError(
                    str(exc)
                ) from exc

            if attempt < self._config.retry_count:

                delay = (
                    self._config.retry_delay
                    * (2 ** (attempt - 1))
                )

                logger.info(
                    "Retrying Telegram request in {} seconds...",
                    delay,
                )

                time.sleep(delay)

        if response is None:

            raise TelegramAPIError(
                "No response received from Telegram."
            )

        logger.info(
            "Telegram responded with HTTP {}.",
            response.status_code,
        )

        try:

            data = response.json()

        except ValueError as exc:

            logger.exception(
                "Telegram returned invalid JSON."
            )

            raise TelegramAPIError(
                "Invalid JSON response from Telegram."
            ) from exc

        if response.status_code == 200:

            logger.info(
                "Telegram notification delivered."
            )

            return True

        description = data.get(
            "description",
            "Unknown Telegram error.",
        )

        logger.error(
            "Telegram API error: {}",
            description,
        )

        status = response.status_code

        if status == 401:

            raise InvalidBotTokenError(
                description
            )

        if status == 400:

            description_lower = description.lower()

            if "chat not found" in description_lower:

                raise InvalidChatIDError(
                    description
                )

            if "message is too long" in description_lower:

                raise MessageTooLongError(
                    description
                )

            if (
                "can't parse entities"
                in description_lower
            ):

                raise MarkdownFormattingError(
                    description
                )

            raise TelegramAPIError(
                description
            )

        if status == 429:

            raise TelegramRateLimitError(
                description
            )

        if status >= 500:

            raise TelegramAPIError(
                description
            )

        raise TelegramAPIError(
            description
        )