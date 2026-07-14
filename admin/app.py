"""
FastAPI application entry point.
"""

from __future__ import annotations

from fastapi import FastAPI
from fastapi.templating import Jinja2Templates
from starlette.middleware.sessions import SessionMiddleware

from config import load_config

from admin.routes import router

config = load_config()

app = FastAPI(
    title="Personal AI Email Summarizer Admin",
    version="1.0.0",
    description="Administration panel for the Personal AI Email Summarizer",
)

app.add_middleware(
    SessionMiddleware,
    secret_key=config.admin.secret_key,
    session_cookie="email_ai_admin",
    same_site="lax",
    https_only=True,
)

templates = Jinja2Templates(
    directory="admin/templates",
)

app.state.templates = templates

app.include_router(router)


def get_app() -> FastAPI:
    """
    Return the configured FastAPI application.
    """

    return app