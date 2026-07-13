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
class AdminConfig:
    """
    Configuration for the Admin Panel.
    """

    username: str
    password: str

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
    retry_count: int
    retry_delay: int

# ==========================================================
# Scheduler Configuration
# ==========================================================

@dataclass(frozen=True)
class SchedulerConfig:
    """
    Configuration for the application scheduler.
    """

    enabled: bool

    run_on_startup: bool

    hour: str

    minute: str

    timezone: str


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

    scheduler: SchedulerConfig

    admin: AdminConfig

    max_emails_per_run: int

    email_retention_days: int


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

    index = 1

    while True:

        email = os.getenv(f"EMAIL_{index}")

        if email is None or email.strip() == "":
            break

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

        index += 1
    if not email_accounts:
        raise ValueError(
            "No email accounts configured."
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
        retry_count=int(
            os.getenv(
                "TELEGRAM_RETRY_COUNT",
                "3",
            )
        ),

        retry_delay=int(
            os.getenv(
                "TELEGRAM_RETRY_DELAY",
                "2",
            )
        ),
    )

    scheduler_config = SchedulerConfig(

        enabled=os.getenv(
            "SCHEDULER_ENABLED",
            "true",
        ).lower() == "true",

        run_on_startup=os.getenv(
            "RUN_ON_STARTUP",
            "true",
        ).lower() == "true",

        hour=os.getenv(
            "SCHEDULE_HOUR",
            "*",
        ),

        minute=os.getenv(
            "SCHEDULE_MINUTE",
            "0",
        ),

        timezone=os.getenv(
            "TIMEZONE",
            "UTC",
        ),
    )

    admin_config = AdminConfig(

        username=get_required_env(
            "ADMIN_USERNAME"
        ),

        password=get_required_env(
            "ADMIN_PASSWORD"
        ),
    )

    return AppConfig(

        email_accounts=email_accounts,

        ai=ai_config,

        telegram=telegram_config,

        scheduler=scheduler_config,

        admin=admin_config,

        max_emails_per_run=int(
            os.getenv(
                "MAX_EMAILS_PER_RUN",
                "20",
            )
        ),
        email_retention_days=int(
            os.getenv(
                "EMAIL_RETENTION_DAYS",
                "30",
            )
        ),
        
    )