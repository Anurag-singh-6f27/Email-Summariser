"""
Test the Groq provider independently.
"""

from datetime import datetime

from config import load_config
from ai.groq import GroqProvider
from mail.models import EmailData


def main() -> None:
    config = load_config()

    provider = GroqProvider(config.ai)

    email = EmailData(
        uid="1",
        message_id="<123@test.com>",
        account_email="me@gmail.com",
        sender_name="GitHub",
        sender_email="noreply@github.com",
        recipient_email="me@gmail.com",
        subject="Pull Request Review Required",
        body="""
Hi,

A new pull request has been opened.

Please review it before Friday.

Repository:
https://github.com/example/repo

Pull Request:
https://github.com/example/repo/pull/123

Thank you.
""",
        received_at=datetime.now(),
        is_html=False,
    )

    result = provider.summarize(email)

    print("\n" + "=" * 70)
    print("SUMMARY RESULT")
    print("=" * 70)

    print(result)

    print("\n" + "=" * 70)
    print("SUMMARY CONTENT")
    print("=" * 70)

    print(result.content)

    print("\n" + "=" * 70)
    print("METADATA")
    print("=" * 70)

    print(result.metadata)


if __name__ == "__main__":
    main()