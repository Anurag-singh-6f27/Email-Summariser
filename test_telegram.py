"""
Test script for the Telegram notification module.
"""

from datetime import datetime

from config import load_config
from mail.models import EmailData

from ai.models import (
    SummaryContent,
    SummaryMetadata,
    SummaryResult,
)

from telegram.service import TelegramService


def main() -> None:
    """
    Test Telegram notification delivery.
    """

    config = load_config()

    telegram = TelegramService(
        config.telegram,
    )

    email = EmailData(
        uid="1",
        message_id="<123@test.com>",
        account_email="me@gmail.com",
        sender_name="GitHub",
        sender_email="noreply@github.com",
        recipient_email="me@gmail.com",
        subject="Pull Request Review Required",
        body="""
A new pull request has been opened.

Repository:
https://github.com/example/repo

Pull Request:
https://github.com/example/repo/pull/123

Please review the pull request before Friday.
""",
        received_at=datetime.now(),
        is_html=False,
    )

    summary = SummaryResult(

        content=SummaryContent(

            concise_summary=(
                "A new pull request has been opened "
                "and requires review before Friday."
            ),

            category="GITHUB",

            priority="MEDIUM",

            action_required=True,

            action_items=[
                "Review the pull request before Friday."
            ],

            important_dates=[
                "Friday"
            ],

            meetings=[],

            financial_items=[],

            important_links=[
                "https://github.com/example/repo",
                "https://github.com/example/repo/pull/123",
            ],

            people=[],

            organizations=[
                "GitHub"
            ],

            notes=[],
        ),

        metadata=SummaryMetadata(

            provider="Gemini",

            model="models/gemini-3.5-flash",

            processing_time_ms=1250.42,

            tokens_used=328,

            success=True,
        ),
    )

    success = telegram.send_email_summary(
        email,
        summary,
    )

    print()
    print("=" * 60)
    print("DELIVERY STATUS")
    print("=" * 60)
    print(success)


if __name__ == "__main__":
    main()