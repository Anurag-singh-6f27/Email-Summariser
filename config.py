"""
Application configuration.

Loads environment variables and exposes a strongly typed
configuration object for the application.
"""

from __future__ import annotations

import os
from dataclasses import dataclass

from dotenv import load_dotenv

load_dotenv()


# ==========================================================
# Email Configuration
# ==========================================================

@dataclass(frozen=True)
class EmailConfig:
    """
    Configuration for a single email account.
    """

    email: str
    password: str
    imap_server: str
    imap_port: int


# ==========================================================
# AI Configuration
# ==========================================================

@dataclass(frozen=True)
class AIConfig:
    """
    Configuration for AI providers.
    """

    # Gemini
    gemini_api_key: str
    gemini_model: str

    # Grok
    groq_api_key: str
    groq_model: str

    # NVIDIA NIM
    nvidia_api_key: str
    nvidia_model: str

    # Runtime Settings
    timeout: int
    max_retries: int
    summary_max_words: int

    # Default Provider
    primary_provider: str


# ==========================================================
# Telegram Configuration
# ==========================================================

@dataclass(frozen=True)
class TelegramConfig:
    """
    Configuration for Telegram Bot.
    """

    bot_token: str
    chat_id: str


# ==========================================================
# Application Configuration
# ==========================================================

@dataclass(frozen=True)
class AppConfig:
    """
    Root configuration object.
    """

    email_accounts: list[EmailConfig]

    ai: AIConfig

    telegram: TelegramConfig

    max_emails_per_run: int


# ==========================================================
# Helpers
# ==========================================================

def get_required_env(variable_name: str) -> str:
    """
    Read an environment variable.

    Raises:
        ValueError if missing.
    """

    value = os.getenv(variable_name)

    if value is None or value.strip() == "":
        raise ValueError(
            f"Missing required environment variable: {variable_name}"
        )

    return value.strip()


# ==========================================================
# Loader
# ==========================================================

def load_config() -> AppConfig:
    """
    Load the complete application configuration.
    """

    email_accounts: list[EmailConfig] = []

    # Change range when adding more email accounts.
    for index in range(1, 2):

        email_accounts.append(

            EmailConfig(

                email=get_required_env(
                    f"EMAIL_{index}"
                ),

                password=get_required_env(
                    f"EMAIL_{index}_PASSWORD"
                ),

                imap_server=get_required_env(
                    f"EMAIL_{index}_IMAP_SERVER"
                ),

                imap_port=int(
                    get_required_env(
                        f"EMAIL_{index}_IMAP_PORT"
                    )
                ),
            )
        )

    ai_config = AIConfig(

        gemini_api_key=get_required_env(
            "GEMINI_API_KEY"
        ),

        gemini_model=os.getenv(
            "GEMINI_MODEL",
            "gemini-2.5-flash",
        ),

        groq_api_key=get_required_env(
            "GROQ_API_KEY"
        ),

        groq_model=os.getenv(
            "GROQ_MODEL",
            "qwen/qwen3-32b",
        ),

        nvidia_api_key=get_required_env(
            "NVIDIA_API_KEY"
        ),

        nvidia_model=os.getenv(
            "NVIDIA_MODEL",
            "openai/gpt-oss-120b",
        ),

        timeout=int(
            os.getenv(
                "AI_TIMEOUT",
                "30",
            )
        ),

        max_retries=int(
            os.getenv(
                "AI_MAX_RETRIES",
                "2",
            )
        ),

        summary_max_words=int(
            os.getenv(
                "SUMMARY_MAX_WORDS",
                "150",
            )
        ),

        primary_provider=os.getenv(
            "PRIMARY_AI_PROVIDER",
            "gemini",
        ),
    )

    telegram_config = TelegramConfig(

        bot_token=get_required_env(
            "TELEGRAM_BOT_TOKEN"
        ),

        chat_id=get_required_env(
            "TELEGRAM_CHAT_ID"
        ),
    )

    return AppConfig(

        email_accounts=email_accounts,

        ai=ai_config,

        telegram=telegram_config,

        max_emails_per_run=int(
            os.getenv(
                "MAX_EMAILS_PER_RUN",
                "20",
            )
        ),
    )