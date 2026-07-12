from database.models import ProcessedEmail

record = ProcessedEmail(
    id=None,
    message_id="<abc@test.com>",
    uid="123",
    account_email="me@gmail.com",
    sender_email="github@noreply.com",
    subject="Test",
    received_at="2026-07-11T18:00:00",
    processed_at=None,
)

print(record)