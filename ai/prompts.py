"""
Prompt templates for AI email summarization.

This module centralizes every prompt used by the AI providers.
Keeping prompts separate from provider implementations makes
them easier to maintain and tune.
"""

from __future__ import annotations

from mail.models import EmailData


# ==========================================================
# Supported Email Categories
# ==========================================================

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


# ==========================================================
# System Prompt
# ==========================================================

SYSTEM_PROMPT = f"""
You are an expert AI assistant that summarizes emails.

Your responsibilities:

1. Read the email carefully.
2. Return ONLY factual information.
3. Never hallucinate or invent details.
4. Ignore signatures.
5. Ignore unsubscribe sections.
6. Ignore tracking information.
7. Ignore email footers.
8. Ignore HTML artifacts.
9. Keep the summary concise (maximum 150 words).
10. Mention deadlines.
11. Mention meeting dates.
12. Mention monetary values.
13. Mention important links only.
14. Mention required actions.
15. Determine the email priority.
16. Classify the email into one of the supported categories.

Priority values:

LOW
MEDIUM
HIGH
CRITICAL

Supported Categories:

{", ".join(EMAIL_CATEGORIES)}

Important:

- Return only factual information.
- Never invent missing details.
- Do not explain your reasoning.
- The response format is enforced by the API.
"""


# ==========================================================
# Prompt Builder
# ==========================================================

def build_summary_prompt(email: EmailData) -> str:
    """
    Build the prompt sent to the AI provider.

    Args:
        email:
            Parsed EmailData object.

    Returns:
        Fully formatted prompt.
    """

    return f"""
{SYSTEM_PROMPT}

==================================================
EMAIL INFORMATION
==================================================

Sender Name:
{email.sender_name}

Sender Email:
{email.sender_email}

Recipient:
{email.recipient_email}

Subject:
{email.subject}

Received At:
{email.received_at}

Body:

{email.body}

==================================================
END OF EMAIL
==================================================
"""