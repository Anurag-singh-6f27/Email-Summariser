from __future__ import annotations

from pydantic import BaseModel


class StatusResponse(BaseModel):
    application: str
    status: str
    configured_accounts: int
    retention_days: int
    max_emails_per_run: int
    primary_ai_provider: str
    scheduler_enabled: bool
    timezone: str