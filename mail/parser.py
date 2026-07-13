"""
Email parsing utilities.

This module converts raw email.message.EmailMessage objects
into standardized EmailData objects.
"""

from __future__ import annotations

from zoneinfo import ZoneInfo

import re
from email.header import decode_header
from email.message import EmailMessage
from email.utils import parseaddr, parsedate_to_datetime

from bs4 import BeautifulSoup

from datetime import datetime

from mail.models import EmailData
from utils.logger import get_logger

logger = get_logger()


def decode_header_value(value: str | None) -> str:
    """
    Decode MIME encoded headers.
    """

    if not value:
        return ""

    decoded = []

    for part, encoding in decode_header(value):
        if isinstance(part, bytes):
            decoded.append(
                part.decode(encoding or "utf-8", errors="replace")
            )
        else:
            decoded.append(part)

    return "".join(decoded).strip()


def extract_email_address(header: str | None) -> str:
    """
    Extract email address.
    """

    _, email_address = parseaddr(header or "")
    return email_address.strip()


def extract_sender_name(header: str | None) -> str:
    """
    Extract sender display name.
    """

    name, _ = parseaddr(header or "")
    return decode_header_value(name)


def normalize_whitespace(text: str) -> str:
    """
    Normalize whitespace.
    """

    text = text.replace("\r\n", "\n")
    text = text.replace("\r", "\n")

    text = re.sub(r"[ \t]+", " ", text)
    text = re.sub(r"\n{3,}", "\n\n", text)

    return text.strip()


def clean_text(text: str) -> str:
    """
    Final cleanup before returning body.
    """

    text = normalize_whitespace(text)
    text = re.sub(r"\n\s*\n+", "\n\n", text)
    return text.strip()


def html_to_text(html: str) -> str:
    """
    Convert HTML to readable text.
    """

    soup = BeautifulSoup(html, "lxml")

    for tag in soup(["script", "style", "img", "svg"]):
        tag.decompose()

    text = soup.get_text(separator=" ",strip=True)

    return clean_text(text)


def decode_payload(part: EmailMessage) -> str:
    """
    Decode a MIME payload.
    """

    payload = part.get_payload(decode=True)

    if payload is None:
        return ""

    charset = part.get_content_charset()

    try:
        return payload.decode(charset or "utf-8", errors="replace")
    except LookupError:
        return payload.decode("utf-8", errors="replace")


def extract_plain_text(message: EmailMessage) -> str:
    """
    Extract plain text from an email.
    """

    if message.is_multipart():

        for part in message.walk():

            content_type = part.get_content_type()

            disposition = (
                part.get_content_disposition() or ""
            ).lower()

            if disposition == "attachment":
                continue

            if content_type == "text/plain":
                return clean_text(
                    decode_payload(part)
                )

        return ""

    if message.get_content_type() == "text/plain":
        return clean_text(
            decode_payload(message)
        )

    return ""


def extract_html_text(message: EmailMessage) -> str:
    """
    Extract HTML body.
    """

    if message.is_multipart():

        for part in message.walk():

            content_type = part.get_content_type()

            disposition = (
                part.get_content_disposition() or ""
            ).lower()

            if disposition == "attachment":
                continue

            if content_type == "text/html":
                return html_to_text(
                    decode_payload(part)
                )

        return ""

    if message.get_content_type() == "text/html":
        return html_to_text(
            decode_payload(message)
        )

    return ""


def parse_email(
    uid: str,
    account_email: str,
    message: EmailMessage,
) -> EmailData:
    """
    Parse a raw EmailMessage into an EmailData object.

    Args:
        uid: IMAP UID of the message.
        account_email: Mailbox from which this email was fetched.
        message: Raw email.message.EmailMessage object.

    Returns:
        Parsed EmailData instance.
    """

    logger.info("Parsing email UID={}", uid)

    try:
        subject = decode_header_value(message.get("Subject"))

        sender = message.get("From", "")
        recipient = message.get("To", "")

        sender_name = extract_sender_name(sender)
        sender_email = extract_email_address(sender)
        recipient_email = extract_email_address(recipient)

        message_id = message.get("Message-ID", "").strip()

        date_header = message.get("Date","")

        try:
            received_at = parsedate_to_datetime(date_header)
            received_at = received_at.astimezone(ZoneInfo("Asia/Kolkata"))
        except Exception:
            logger.warning(
                "Invalid date header for UID={}. Using current time.",
                uid,
            )

            received_at = datetime.now()

        body = extract_plain_text(message)

        is_html = False

        if not body:
            body = extract_html_text(message)
            is_html = True

        body = clean_text(body)

        if not subject:
            logger.warning("Email UID={} has no subject.", uid)

        if not sender_email:
            logger.warning("Email UID={} has no sender.", uid)

        if not body:
            logger.warning("Email UID={} has empty body.", uid)
        
        logger.info("Mailbox Account : {}", account_email)
        logger.info("To Header       : {}", message.get("To"))
        logger.info("Parsed Recipient: {}", recipient_email)
        logger.info("Date Header     : {}", date_header)
        logger.info("Parsed Date     : {}", received_at)


        email_data = EmailData(
            uid=uid,
            message_id=message_id,
            account_email=account_email,
            sender_name=sender_name,
            sender_email=sender_email,
            recipient_email=recipient_email,
            subject=subject,
            body=body,
            received_at=received_at,
            is_html=is_html,
        )

        logger.info(
            "Parsed email '{}' from {}",
            subject or "(No Subject)",
            sender_email or "(Unknown)",
        )

        return email_data

    except Exception:
        logger.exception("Failed to parse email UID={}", uid)
        raise