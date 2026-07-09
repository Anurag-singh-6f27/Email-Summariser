"""
Configuration management for the AI Email Summarizer.

This module is responsible for:
- Loading environment variables
- Validating required configuration
- Providing a strongly typed configuration object
"""

from __future__ import annotations

import os
from dataclasses import dataclass

from dotenv import load_dotenv


load_dotenv()


@dataclass(frozen=True)
class EmailConfig:
    """Configuration for a single email account."""

    email: str
    password: str
    imap_server: str
    imap_port: int


@dataclass(frozen=True)
class AIConfig:
    """Configuration for AI providers."""

    gemini_api_key: str
    grok_api_key: str


@dataclass(frozen=True)
class TelegramConfig:
    """Configuration for Telegram Bot."""

    bot_token: str
    chat_id: str


@dataclass(frozen=True)
class AppConfig:
    """Complete application configuration."""

    email_accounts: list[EmailConfig]
    ai: AIConfig
    telegram: TelegramConfig


def get_required_env(variable_name: str) -> str:
    """
    Read and validate a required environment variable.

    Args:
        variable_name: Name of the environment variable.

    Returns:
        The environment variable value.

    Raises:
        ValueError: If the variable is missing or empty.
    """
    value = os.getenv(variable_name)

    if value is None or value.strip() == "":
        raise ValueError(
            f"Missing required environment variable: {variable_name}"
        )

    return value.strip()


def load_config() -> AppConfig:
    """
    Load and validate the complete application configuration.

    Returns:
        AppConfig containing all application settings.
    """

    email_accounts = []

    for index in range(1, 4):
        account = EmailConfig(
            email=get_required_env(f"EMAIL_{index}"),
            password=get_required_env(f"EMAIL_{index}_PASSWORD"),
            imap_server=get_required_env(f"EMAIL_{index}_IMAP_SERVER"),
            imap_port=int(get_required_env(f"EMAIL_{index}_IMAP_PORT"))
        )

        email_accounts.append(account)

    ai_config = AIConfig(
        gemini_api_key=get_required_env("GEMINI_API_KEY"),
        grok_api_key=get_required_env("GROK_API_KEY"),
    )

    telegram_config = TelegramConfig(
        bot_token=get_required_env("TELEGRAM_BOT_TOKEN"),
        chat_id=get_required_env("TELEGRAM_CHAT_ID"),
    )

    return AppConfig(
        email_accounts=email_accounts,
        ai=ai_config,
        telegram=telegram_config,
    )