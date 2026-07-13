"""
Authentication utilities for the Admin Panel.
"""

from __future__ import annotations

from config import load_config

config = load_config()


from config import AppConfig


def authenticate(
    username: str,
    password: str,
    config: AppConfig,
) -> bool:
    """
    Validate administrator credentials.
    """

    return (
        username == config.admin.username
        and password == config.admin.password
    )