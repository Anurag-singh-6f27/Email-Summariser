"""
Google Gemini AI provider.

Implements the BaseAIProvider interface using the
Google GenAI SDK.
"""

from __future__ import annotations

import time

from google import genai
from google.genai import types

from config import AIConfig
from mail.models import EmailData

from ai.schema import SummarySchema

from ai.base_provider import BaseAIProvider
from ai.exceptions import (
    AIServiceError,
    EmptySummaryError,
    InvalidAPIKeyError,
    InvalidResponseError,
    ModelUnavailableError,
    NetworkTimeoutError,
    RateLimitError,
)
from ai.models import (
    SummaryContent,
    SummaryMetadata,
    SummaryResult,
)
from ai.prompts import build_summary_prompt
from utils.logger import get_logger

logger = get_logger()


class GeminiProvider(BaseAIProvider):
    """
    Google Gemini implementation of BaseAIProvider.
    """

    def __init__(self, config: AIConfig) -> None:
        """
        Initialize the Gemini provider.

        Args:
            config:
                AI configuration containing API key,
                model name, timeout and retry settings.
        """

        self._config = config

        self._provider_name = "Gemini"

        self._configure_client()
    


    @property
    def provider_name(self) -> str:
        """
        Return provider name.
        """

        return self._provider_name

    def _configure_client(self) -> None:
        """
        Configure the Google GenAI client.
        """

        logger.info("Initializing Gemini client...")

        try:

            self._client = genai.Client(
                api_key=self._config.gemini_api_key,
            )

            logger.info(
                "Gemini client initialized successfully."
            )

            logger.info(
                "Using Gemini model '{}'.",
                self._config.gemini_model,
            )

        except Exception as exc:

            logger.exception(
                "Failed to initialize Gemini client."
            )

            raise InvalidAPIKeyError(
                str(exc)
            ) from exc
        
    def _generate_response(
        self,
        prompt: str,
    ) -> tuple[SummarySchema, float]:
        """
        Send a prompt to Gemini and return the raw response.

        Args:
            prompt:
                Prompt sent to Gemini.

        Returns:
            Tuple containing:
                - Parsed SummarySchema
                - Processing time in milliseconds.
        """

        logger.info("Sending request to Gemini...")

        start_time = time.perf_counter()

        try:

            response = self._client.models.generate_content(

                model=self._config.gemini_model,

                contents=prompt,

                config=types.GenerateContentConfig(
                   temperature=0.2,
                   response_mime_type="application/json",
                   response_schema=SummarySchema,
                ),
            )

            processing_time = (
                time.perf_counter() - start_time
            ) * 1000

            if response.parsed is None:
                raise EmptySummaryError(
                    "Gemini returned an empty response."
                )

            logger.info(
                "Gemini response received in {:.2f} ms.",
                processing_time,
            )

            return response.parsed, processing_time

        except EmptySummaryError:
            raise

        except Exception as exc:

            logger.exception(
                "Gemini request failed."
            )

            message = str(exc).lower()

            if "api key" in message or "authentication" in message:
                raise InvalidAPIKeyError(str(exc)) from exc

            if "quota" in message or "429" in message:
                raise RateLimitError(str(exc)) from exc

            if "timeout" in message:
                raise NetworkTimeoutError(str(exc)) from exc

            if (
                "404" in message
                or "not found" in message
                or "unsupported model" in message
            ):
                raise ModelUnavailableError(str(exc)) from exc

            raise AIServiceError(str(exc)) from exc
        
    def _parse_response(
        self,
        response: SummarySchema,
    ) -> SummaryContent:
        """
        Convert the validated SummarySchema returned by Gemini
        into the application's SummaryContent model.

        Args:
            response:
                Structured response returned by Gemini.

        Returns:
            SummaryContent
        """

        logger.info("Converting Gemini response to SummaryContent...")

        try:
            return SummaryContent(
                concise_summary=response.concise_summary,
                category=response.category,
                priority=response.priority,
                action_required=response.action_required,
                action_items=response.action_items,
                important_dates=response.important_dates,
                meetings=response.meetings,
                financial_items=response.financial_items,
                important_links=response.important_links,
                people=response.people,
                organizations=response.organizations,
                notes=response.notes,
            )

        except Exception as exc:
            logger.exception(
                "Failed to convert Gemini response."
            )

            raise InvalidResponseError(
                "Invalid structured response returned by Gemini."
            ) from exc


    def _build_result(
        self,
        content: SummaryContent,
        processing_time_ms: float,
    ) -> SummaryResult:
        """
        Build the final SummaryResult.
        """

        metadata = SummaryMetadata(
            provider=self.provider_name,
            model=self._config.gemini_model,
            processing_time_ms=processing_time_ms,
            tokens_used=None,
            success=True,
            error=None,
        )

        return SummaryResult(
            content=content,
            metadata=metadata,
        )

    def summarize(
        self,
        email: EmailData,
    ) -> SummaryResult:
        """
        Generate a structured summary for an email.
        """

        logger.info(
            "Generating summary for '{}'.",
            email.subject,
        )

        prompt = build_summary_prompt(email)

        raw_response, processing_time = self._generate_response(
            prompt
        )

        content = self._parse_response(
            raw_response
        )

        result = self._build_result(
            content,
            processing_time,
        )

        logger.info(
            "Summary generated successfully."
        )

        return result