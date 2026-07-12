
from __future__ import annotations

import json
import time

from openai import OpenAI

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
from ai.groq_prompts import build_summary_prompt
from utils.logger import get_logger

logger = get_logger()


class NvidiaProvider(BaseAIProvider):
    """
    nvidia implementation of BaseAIProvider.
    """

    def __init__(
        self,
        config: AIConfig,
    ) -> None:

        self._config = config
        self._provider_name = "NVIDIA"

        self._configure_client()

    @property
    def provider_name(self) -> str:
        return self._provider_name

    def _configure_client(self) -> None:
        """
        Initialize the NVIDIA client.
        """

        logger.info("Initializing NVIDIA client...")

        try:

            self._client = OpenAI(
                api_key=self._config.nvidia_api_key,
                base_url="https://integrate.api.nvidia.com/v1",
            )

            logger.info(
                "NVIDIA client initialized successfully."
            )

            logger.info(
                "Using NVIDIA model '{}'.",
                self._config.nvidia_model,
            )

        except Exception as exc:

            logger.exception(
                "Failed to initialize NVIDIA client."
            )

            raise InvalidAPIKeyError(
                str(exc)
            ) from exc

    def _generate_response(
        self,
        prompt: str,
    ) -> tuple[SummarySchema, float]:
        """
        Send a prompt to NVIDIA and return the parsed response.

        Args:
            prompt:
                Prompt sent to NVIDIA.

        Returns:
            Tuple containing:
                - Parsed SummarySchema
                - Processing time in milliseconds.
        """

        logger.info("Sending request to NVIDIA...")

        start_time = time.perf_counter()

        try:
            completion = self._client.chat.completions.create(

                model=self._config.nvidia_model,

                messages=[
                    {
                        "role": "user",
                        "content": prompt,
                    },
                ],

                temperature=0.2,

                extra_body={
                    "reasoning_effort": "low",
                },
            )

            processing_time = (
                time.perf_counter() - start_time
            ) * 1000

            content = completion.choices[0].message.content
            logger.info("Raw NVIDIA response:\n{}", content)

            if not content:
                raise EmptySummaryError(
                    "NVIDIA returned an empty response."
                )

            logger.info(
                "NVIDIA response received in {:.2f} ms.",
                processing_time,
            )

            # Remove markdown code fences if the model adds them.
            content = content.strip()

            if content.startswith("```json"):
                content = content[7:]

            if content.startswith("```"):
                content = content[3:]

            if content.endswith("```"):
                content = content[:-3]

            content = content.strip()

            try:
                data = json.loads(content)
                logger.info(
                      "Parsed JSON:\n{}",
                      json.dumps(data, indent=4),
                  )

            except json.JSONDecodeError as exc:
                raise InvalidResponseError(
                    "NVIDIA returned invalid JSON."
                ) from exc
            
            required_fields = {
                "concise_summary",
                "category",
                "priority",
                "action_required",
                "action_items",
                "important_dates",
                "meetings",
                "financial_items",
                "important_links",
                "people",
                "organizations",
                "notes",
            }
            missing = required_fields.difference(data.keys())

            if missing:
                raise InvalidResponseError(
                      f"NVIDIA returned an invalid schema. Missing fields: {sorted(missing)}"
                  )

            parsed = SummarySchema(**data)

            return parsed, processing_time

        except EmptySummaryError:
            raise

        except Exception as exc:

            logger.exception(
                "NVIDIA request failed."
            )

            message = str(exc).lower()

            if (
                "api key" in message
                or "authentication" in message
            ):
                raise InvalidAPIKeyError(
                    str(exc)
                ) from exc

            if (
                "quota" in message
                or "429" in message
            ):
                raise RateLimitError(
                    str(exc)
                ) from exc

            if "timeout" in message:
                raise NetworkTimeoutError(
                    str(exc)
                ) from exc

            if (
                "404" in message
                or "not found" in message
            ):
                raise ModelUnavailableError(
                    str(exc)
                ) from exc

            raise AIServiceError(
                str(exc)
            ) from exc

    def _parse_response(
        self,
        response: SummarySchema,
    ) -> SummaryContent:
        """
        Convert SummarySchema into SummaryContent.
        """

        logger.info(
            "Converting NVIDIA response to SummaryContent..."
        )

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
                "Failed to convert NVIDIA response."
            )

            raise InvalidResponseError(
                "Invalid structured response returned by NVIDIA."
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
            model=self._config.nvidia_model,
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
        Generate a structured summary.
        """

        logger.info(
            "Generating summary for '{}'.",
            email.subject,
        )

        prompt = build_summary_prompt(
            email
        )

        parsed_response, processing_time = (
            self._generate_response(prompt)
        )

        content = self._parse_response(
            parsed_response
        )

        result = self._build_result(
            content,
            processing_time,
        )

        logger.info(
            "Summary generated successfully."
        )

        return result