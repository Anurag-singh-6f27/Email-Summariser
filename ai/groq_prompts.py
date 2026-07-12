"""
Prompt templates for Groq/OpenAI-compatible models.

Unlike Gemini Structured Output, Groq relies entirely on
prompt engineering to return valid JSON.
"""

from __future__ import annotations

import json

from mail.models import EmailData


EMAIL_CATEGORIES = [
    "JOB",
    "INTERVIEW",
    "GITHUB",
    "BANK",
    "FINANCE",
    "PAYMENT",
    "SHOPPING",
    "ORDER",
    "MEETING",
    "CALENDAR",
    "COURSE",
    "EDUCATION",
    "SECURITY",
    "OTP",
    "SOCIAL",
    "NEWSLETTER",
    "PROMOTION",
    "PERSONAL",
    "UNKNOWN",
]


EXPECTED_JSON_SCHEMA = {
    "concise_summary": "",
    "category": "",
    "priority": "",
    "action_required": False,
    "action_items": [],
    "important_dates": [],
    "meetings": [],
    "financial_items": [],
    "important_links": [],
    "people": [],
    "organizations": [],
    "notes": [],
}


SYSTEM_PROMPT = f"""
You are an email summarization engine.

Your task is to analyze an email and return ONLY ONE valid JSON object.

Rules:

1. Never explain your reasoning.
2. Never output <think>.
3. Never output markdown.
4. Never wrap JSON inside ``` blocks.
5. Never rename keys.
6. Never omit keys.
7. Never invent keys.
8. Every key is mandatory.
9. Return only factual information.
10. Ignore signatures.
11. Ignore unsubscribe sections.
12. Ignore HTML artifacts.
13. Keep summary under 150 words.

Priority values:

LOW
MEDIUM
HIGH
CRITICAL

Categories:

{", ".join(EMAIL_CATEGORIES)}
"""


def build_summary_prompt(
    email: EmailData,
) -> str:
    """
    Build the prompt sent to Groq.
    """

    schema = json.dumps(
        EXPECTED_JSON_SCHEMA,
        indent=4,
    )

    return f"""
{SYSTEM_PROMPT}

EMAIL

Sender:
{email.sender_name}

Sender Email:
{email.sender_email}

Recipient:
{email.recipient_email}

Subject:
{email.subject}

Body:

{email.body}

Return EXACTLY this JSON schema.

{schema}

Rules:

- Do not change field names.
- Use false for booleans.
- Use [] for arrays.
- Use "" for strings.
- Return ONLY JSON.
"""