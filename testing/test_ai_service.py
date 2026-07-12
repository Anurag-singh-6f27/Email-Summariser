"""
Test script for the AIService.

Verifies:

- Provider initialization
- Provider selection
- Email summarization
- Returned SummaryResult
"""

from datetime import datetime

from config import load_config
from mail.models import EmailData

from ai.service import AIService


def main() -> None:
    """
    Test the AI service.
    """

    config = load_config()

    service = AIService(config.ai)

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

    result = service.summarize(email)

    print()
    print("=" * 70)
    print("ACTIVE PROVIDER")
    print("=" * 70)
    print(result.metadata.provider)

    print()
    print("=" * 70)
    print("SUMMARY RESULT")
    print("=" * 70)
    print(result)

    print()
    print("=" * 70)
    print("SUMMARY CONTENT")
    print("=" * 70)
    print(result.content)

    print()
    print("=" * 70)
    print("METADATA")
    print("=" * 70)
    print(result.metadata)


if __name__ == "__main__":
    main()