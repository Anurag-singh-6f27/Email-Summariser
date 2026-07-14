"""
Authentication utilities for the Admin Panel.
"""

from __future__ import annotations

from fastapi import Request

from config import AppConfig

from fastapi.responses import RedirectResponse

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


def login(
    request: Request,
) -> None:
    """
    Create an authenticated session.
    """

    request.session["authenticated"] = True


def logout(
    request: Request,
) -> None:
    """
    Destroy the authenticated session.
    """

    request.session.clear()


def is_authenticated(
    request: Request,
) -> bool:
    """
    Return whether the current user is authenticated.
    """

    return request.session.get(
        "authenticated",
        False,
    )

def require_login(
    request: Request,
):
    """
    Redirect unauthenticated users to the login page.
    """

    if not is_authenticated(request):

        return RedirectResponse(
            "/login",
            status_code=303,
        )

    return None