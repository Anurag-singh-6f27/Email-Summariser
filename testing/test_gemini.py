from datetime import datetime

from ai.gemini import GeminiProvider
from config import load_config
from mail.models import EmailData

config = load_config()
provider = GeminiProvider(config.ai)

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

Please review it before Friday.

https://github.com/example/repo/pull/123
""",
    received_at=datetime.now(),
    is_html=False,
)

result = provider.summarize(email)

print(result)