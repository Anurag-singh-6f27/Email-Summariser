"""
Abstract base class for all AI providers.

Every AI provider must implement this interface.
"""

from __future__ import annotations

from abc import ABC, abstractmethod

from mail.models import EmailData

from ai.models import SummaryResult


class BaseAIProvider(ABC):
    """
    Base interface implemented by every AI provider.
    """

    @property
    @abstractmethod
    def provider_name(self) -> str:
        """
        Human-readable provider name.
        """
        raise NotImplementedError

    @abstractmethod
    def summarize(
        self,
        email: EmailData,
    ) -> SummaryResult:
        """
        Generate a structured summary.

        Args:
            email:
                Parsed EmailData object.

        Returns:
            SummaryResult
        """
        raise NotImplementedError