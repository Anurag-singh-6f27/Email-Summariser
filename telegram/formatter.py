"""
Telegram message formatter.

Converts EmailData and SummaryResult into a formatted
Telegram message.
"""

from __future__ import annotations

import re

from mail.models import EmailData
from ai.models import SummaryResult

from telegram.models import TelegramMessage


# ==========================================================
# MarkdownV2 Escaping
# ==========================================================

_MARKDOWN_PATTERN = re.compile(r"([_*\[\]()~`>#+\-=|{}.!])")


def escape_markdown(
    text: str,
) -> str:
    """
    Escape Telegram MarkdownV2 special characters.
    """

    if not text:
        return ""

    return _MARKDOWN_PATTERN.sub(
        r"\\\1",
        text,
    )


# ==========================================================
# Telegram Formatter
# ==========================================================

class TelegramFormatter:
    """
    Formats AI summaries into Telegram messages.
    """

    MAX_MESSAGE_LENGTH = 4096

    def format(
        self,
        email: EmailData,
        summary: SummaryResult,
    ) -> TelegramMessage:
        """
        Convert EmailData and SummaryResult into a
        TelegramMessage.
        """

        content = summary.content
        metadata = summary.metadata

        lines: list[str] = [

            "📧 *New Email*",
            "",

            f"📥 *Inbox:* {escape_markdown(email.recipient_email)}",

            f"👤 *From:* {escape_markdown(email.sender_name)}",

            f"📨 *Email:* {escape_markdown(email.sender_email)}",

            f"📌 *Subject:* {escape_markdown(email.subject)}",

            "",

            f"🏷️ *Category:* {escape_markdown(content.category)}",

            f"⚡ *Priority:* {escape_markdown(content.priority)}",

            "",

            "🤖 *AI Summary*",

            escape_markdown(
                content.concise_summary
            ),
        ]

        if content.action_required:

            lines.extend([
                "",
                "✅ *Action Required*",
            ])

            for item in content.action_items:

                lines.append(
                    f"• {escape_markdown(item)}"
                )

        if content.important_dates:

            lines.extend([
                "",
                "📅 *Important Dates*",
            ])

            for item in content.important_dates:

                lines.append(
                    f"• {escape_markdown(item)}"
                )

        if content.meetings:

            lines.extend([
                "",
                "📆 *Meetings*",
            ])

            for item in content.meetings:

                lines.append(
                    f"• {escape_markdown(item)}"
                )

        if content.financial_items:

            lines.extend([
                "",
                "💰 *Financial Items*",
            ])

            for item in content.financial_items:

                lines.append(
                    f"• {escape_markdown(item)}"
                )

        if content.important_links:

            lines.extend([
                "",
                "🔗 *Important Links*",
            ])

            for item in content.important_links:

                lines.append(
                    escape_markdown(item)
                )

        if content.people:

            lines.extend([
                "",
                "👥 *People*",
            ])

            for item in content.people:

                lines.append(
                    f"• {escape_markdown(item)}"
                )

        if content.organizations:

            lines.extend([
                "",
                "🏢 *Organizations*",
            ])

            for item in content.organizations:

                lines.append(
                    f"• {escape_markdown(item)}"
                )

        if content.notes:

            lines.extend([
                "",
                "📝 *Notes*",
            ])

            for item in content.notes:

                lines.append(
                    f"• {escape_markdown(item)}"
                )

        lines.extend([
            "",
            f"🧠 *Provider:* {escape_markdown(metadata.provider)}",
        ])

        text = "\n".join(lines)

        if len(text) > self.MAX_MESSAGE_LENGTH:

            text = (
                text[: self.MAX_MESSAGE_LENGTH - 3]
                + "..."
            )

        return TelegramMessage(
            text=text,
            parse_mode="MarkdownV2",
            disable_web_page_preview=True,
        )