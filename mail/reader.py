"""
IMAP email reader.

Responsible for:

- Connecting to IMAP servers
- Authenticating users
- Fetching unread emails
- Returning parsed EmailData objects
"""

from __future__ import annotations

from email import policy
from email.parser import BytesParser
import imaplib
import socket

from typing import List

from config import AppConfig, EmailConfig
from mail.models import EmailData
from mail.parser import parse_email
from utils.logger import get_logger

logger = get_logger()


class EmailReader:
    """
    Reads unread emails from configured accounts.
    """

    def __init__(self, config: AppConfig) -> None:
        self.config = config

    def fetch_all_unread(self) -> List[EmailData]:
        """
        Fetch unread emails from every configured account.
        """

        emails: List[EmailData] = []

        for account in self.config.email_accounts:

            logger.info(
                "Connecting to account {}",
                account.email,
            )

            try:

                emails.extend(
                    self._fetch_account_emails(account)
                )

            except Exception:

                logger.exception(
                    "Failed reading {}",
                    account.email,
                )

        logger.info(
            "Fetched {} unread emails.",
            len(emails),
        )

        return emails

    def _connect(
        self,
        account: EmailConfig,
    ) -> imaplib.IMAP4_SSL:
        """
        Establish an IMAP SSL connection.
        """

        try:

            client = imaplib.IMAP4_SSL(
                account.imap_server,
                account.imap_port,
            )

            client.login(
                account.email,
                account.password,
            )

            logger.info(
                "Authentication successful for {}",
                account.email,
            )

            return client

        except imaplib.IMAP4.error as exc:

            logger.error(
                "Authentication failed for {}",
                account.email,
            )

            raise RuntimeError(
                f"Authentication failed for {account.email}"
            ) from exc

        except socket.timeout as exc:

            logger.exception(
                "Timeout while connecting to {}",
                account.email,
            )

            raise RuntimeError(
                f"Timeout connecting to {account.email}"
            ) from exc

    def _fetch_account_emails(
        self,
        account: EmailConfig,
    ) -> List[EmailData]:
        """
        Fetch unread emails for one account.
        """

        client = self._connect(account)

        parsed_emails: List[EmailData] = []

        try:

            status, _ = client.select("INBOX")

            if status != "OK":
                raise RuntimeError(
                    "Unable to open inbox."
                )

            logger.info(
                "Inbox selected for {}",
                account.email,
            )

            status, data = client.uid(
                "search",
                None,
                "UNSEEN",
            )

            if status != "OK":
                raise RuntimeError(
                    "Unable to search mailbox."
                )

            uid_list = data[0].split()

            uid_list.reverse()

            uid_list = uid_list[: self.config.max_emails_per_run]

            logger.info(
                "{} unread emails found.",
                len(uid_list),
            )
            for uid in uid_list:

                uid_str = uid.decode()

                status, message_data = client.uid(
                    "fetch",
                    uid,
                    "(RFC822)",
                )

                if status != "OK":
                    logger.warning(
                        "Failed to fetch email UID={}",
                        uid_str,
                    )
                    continue

                raw_email = None

                for response in message_data:
                    if (
                        isinstance(response, tuple)
                        and len(response) == 2
                    ):
                        raw_email = response[1]
                        break

                if raw_email is None:
                    logger.warning(
                        "Empty RFC822 response for UID={}",
                        uid_str,
                    )
                    continue

                try:
                    message = BytesParser(
                        policy=policy.default
                    ).parsebytes(raw_email)

                    parsed_email = parse_email(
                        uid=uid_str,
                        account_email=account.email,
                        message=message,
                    )

                    parsed_emails.append(parsed_email)

                except Exception:
                    logger.exception(
                        "Failed parsing UID={}",
                        uid_str,
                    )

            return parsed_emails

        finally:

            try:
                client.close()
            except Exception:
                pass

            try:
                client.logout()
            except Exception:
                pass

            logger.info(
                "Connection closed for {}",
                account.email,
            )