"""
Central AI service.

Provides a single entry point for email summarization while
handling provider selection, retries, and automatic fallback.
"""

from __future__ import annotations

from config import AIConfig
from mail.models import EmailData

from ai.base_provider import BaseAIProvider
from ai.exceptions import (
    AIServiceError,
    NetworkTimeoutError,
    ProviderNotConfiguredError,
    RateLimitError,
)
from ai.models import SummaryResult

from ai.gemini import GeminiProvider
from ai.groq import GroqProvider
from ai.nvidia import NvidiaProvider

from utils.logger import get_logger

logger = get_logger()


class AIService:
    """
    Coordinates all AI providers.

    Handles:

    - Provider initialization
    - Provider selection
    - Retry logic
    - Automatic fallback
    """

    def __init__(
        self,
        config: AIConfig,
    ) -> None:

        self._config = config

        self._providers: dict[str, BaseAIProvider] = {

            "gemini": GeminiProvider(config),

            "groq": GroqProvider(config),

            "nvidia": NvidiaProvider(config),
        }

        self._provider_order = self._build_provider_order()

        logger.info(
            "Primary AI provider: {}",
            self._provider_order[0],
        )

    def _build_provider_order(
        self,
    ) -> list[str]:
        """
        Build provider order.

        Primary provider is first.
        Remaining providers become fallbacks.
        """

        primary = (
            self._config.primary_provider
            .strip()
            .lower()
        )

        if primary not in self._providers:

            raise ProviderNotConfiguredError(
                f"Unknown provider '{primary}'."
            )

        order = [primary]

        for provider in self._providers:

            if provider != primary:

                order.append(provider)

        return order

    def summarize(
        self,
        email: EmailData,
    ) -> SummaryResult:
        """
        Summarize an email.

        Tries providers in configured order.

        Automatically retries transient failures.

        Automatically falls back if a provider fails.
        """

        last_exception: Exception | None = None

        for provider_name in self._provider_order:

            provider = self._providers[provider_name]

            logger.info(
                "Trying provider '{}'.",
                provider_name,
            )

            attempt = 0

            while attempt <= self._config.max_retries:

                try:

                    logger.info(
                        "Attempt {} using {}.",
                        attempt + 1,
                        provider_name,
                    )

                    return provider.summarize(email)

                except (
                    NetworkTimeoutError,
                    RateLimitError,
                ) as exc:

                    attempt += 1

                    last_exception = exc

                    logger.warning(
                        "{} failed (attempt {}/{}): {}",
                        provider_name,
                        attempt,
                        self._config.max_retries,
                        exc,
                    )

                    if attempt > self._config.max_retries:

                        logger.error(
                            "{} exceeded retry limit.",
                            provider_name,
                        )

                except Exception as exc:

                    last_exception = exc

                    logger.error(
                        "{} failed: {}",
                        provider_name,
                        exc,
                    )

                    break

        raise AIServiceError(
            f"All AI providers failed. Last error: {last_exception}"
        )