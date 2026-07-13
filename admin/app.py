"""
FastAPI application entry point.
"""

from __future__ import annotations

from fastapi import FastAPI
from fastapi.templating import Jinja2Templates

from admin.routes import router


app = FastAPI(
    title="Personal AI Email Summarizer Admin",
    version="1.0.0",
    description="Administration panel for the Personal AI Email Summarizer",
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