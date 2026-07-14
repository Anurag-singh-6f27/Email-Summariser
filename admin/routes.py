"""
Admin API routes.
"""

from __future__ import annotations

from datetime import datetime

from fastapi import APIRouter

from config import load_config

from admin.schemas import StatusResponse
from fastapi import HTTPException

from admin import state
from fastapi import HTTPException

from admin.auth import authenticate
from admin.log_service import get_log_page

from fastapi import Request

from fastapi.responses import RedirectResponse

from fastapi.responses import HTMLResponse
from database.connection import DatabaseManager
from database.repository import ProcessedEmailRepository
router = APIRouter()

config = load_config()

database = DatabaseManager()
repository = ProcessedEmailRepository(database)
@router.get("/")
def home() -> dict[str, str]:

    return {
        "message": "Personal AI Email Summarizer Admin Panel"
    }


@router.get("/health")
def health() -> dict[str, str]:

    return {
        "status": "healthy",
        "service": "Personal AI Email Summarizer Admin",
        "timestamp": datetime.now().isoformat(),
    }

@router.post("/pipeline/run")
def run_pipeline() -> dict[str, str]:
    """
    Execute the pipeline immediately.
    """

    if state.scheduler is None:

        raise HTTPException(
            status_code=503,
            detail="Scheduler is not connected.",
        )

    state.scheduler.run_pipeline()

    return {
        "message": "Pipeline started successfully."
    }

@router.get(
      "/status",
    response_model=StatusResponse,
    )
def status() -> StatusResponse:

  return StatusResponse(
      application="Personal AI Email Summarizer",
      status="Running",
      configured_accounts=len(config.email_accounts),
      retention_days=config.email_retention_days,
      max_emails_per_run=config.max_emails_per_run,
      primary_ai_provider=config.ai.primary_provider,
      scheduler_enabled=config.scheduler.enabled,
      timezone=config.scheduler.timezone,
  )

@router.get(
    "/dashboard",
    response_class=HTMLResponse,
)
def dashboard(
    request: Request,
):

    dashboard = {

        "pipeline_running": (
            state.scheduler.is_pipeline_running()
            if state.scheduler
            else False
        ),

        "scheduler_running": (
            state.scheduler.is_running()
            if state.scheduler
            else False
        ),

        "scheduler_paused": (
            state.scheduler.is_paused()
            if state.scheduler
            else False
        ),

        "email_accounts": len(
            config.email_accounts
        ),

        "primary_provider": (
            config.ai.primary_provider.upper()
        ),

        "processed_emails": (
            repository.count_processed()
        ),

        "timezone": (
            config.scheduler.timezone
        ),

        "max_emails": (
            config.max_emails_per_run
        ),

        "retention_days": (
            config.email_retention_days
        ),
    }

    return request.app.state.templates.TemplateResponse(
        request=request,
        name="dashboard.html",
        context={
            "dashboard": dashboard,
        },
    )

@router.post("/login")
def login(
    username: str,
    password: str,
):
    """
    Authenticate the administrator.
    """

    if not authenticate(
        username,
        password,
        config,
    ):
        raise HTTPException(
            status_code=401,
            detail="Invalid username or password.",
        )

    return {
        "message": "Login successful."
    }

@router.get(
    "/statistics",
    response_class=HTMLResponse,
)
def statistics(
    request: Request,
):

    stats = {
        "configured_accounts": len(config.email_accounts),
        "retention_days": config.email_retention_days,
        "max_emails_per_run": config.max_emails_per_run,
        "primary_ai_provider": config.ai.primary_provider,
        "scheduler_enabled": config.scheduler.enabled,
        "timezone": config.scheduler.timezone,
    }

    return request.app.state.templates.TemplateResponse(
        request=request,
        name="statistics.html",
        context={
            "stats": stats,
        },
    )


@router.get(
    "/emails",
    response_class=HTMLResponse,
)
def emails(
    request: Request,
    page: int = 1,
):

    PAGE_SIZE = 20

    emails = repository.get_processed_page(
        page=page,
        page_size=PAGE_SIZE,
    )

    total_emails = repository.count_processed()

    total_pages = (
        total_emails + PAGE_SIZE - 1
    ) // PAGE_SIZE

    return request.app.state.templates.TemplateResponse(
        request=request,
        name="emails.html",
        context={
            "emails": emails,
            "page": page,
            "page_size": PAGE_SIZE,
            "total_pages": total_pages,
            "total_emails": total_emails,
        },
    )


@router.get(
    "/scheduler",
    response_class=HTMLResponse,
)
def scheduler(
    request: Request,
):

    scheduler = {

        "enabled": (
            state.scheduler.is_running()
            if state.scheduler is not None
            else False
        ),

        "paused": (
            state.scheduler.is_paused()
            if state.scheduler is not None
            else False
        ),

        "pipeline_running": (
            state.scheduler.is_pipeline_running()
            if state.scheduler is not None
            else False
        ),

        "hour": config.scheduler.hour,

        "minute": config.scheduler.minute,

        "timezone": config.scheduler.timezone,

        "run_on_startup": config.scheduler.run_on_startup,
    }

    return request.app.state.templates.TemplateResponse(
        request=request,
        name="scheduler.html",
        context={
            "scheduler": scheduler,
        },
    )


@router.get(
    "/providers",
    response_class=HTMLResponse,
)
def providers(
    request: Request,
):

    providers = [
        {
            "name": "Groq",
            "configured": bool(config.ai.groq_api_key),
            "primary": config.ai.primary_provider.lower() == "groq",
            "model": config.ai.groq_model,
        },
        {
            "name": "Gemini",
            "configured": bool(config.ai.gemini_api_key),
            "primary": config.ai.primary_provider.lower() == "gemini",
            "model": config.ai.gemini_model,
        },
        {
            "name": "NVIDIA",
            "configured": bool(config.ai.nvidia_api_key),
            "primary": config.ai.primary_provider.lower() == "nvidia",
            "model": config.ai.nvidia_model,
        },
    ]

    return request.app.state.templates.TemplateResponse(
        request=request,
        name="providers.html",
        context={
            "providers": providers,
        },
    )


@router.get(
    "/configuration",
    response_class=HTMLResponse,
)
def configuration(
    request: Request,
):

    return request.app.state.templates.TemplateResponse(
        request=request,
        name="configuration.html",
        context={
            "config": config,
        },
    )

@router.get(
    "/logs",
    response_class=HTMLResponse,
)
def logs(
    request: Request,
    page: int = 1,
):

    PAGE_SIZE = 100

    logs, total_logs = get_log_page(
        page,
        PAGE_SIZE,
    )

    total_pages = (
        total_logs + PAGE_SIZE - 1
    ) // PAGE_SIZE

    return request.app.state.templates.TemplateResponse(
        request=request,
        name="logs.html",
        context={
            "logs": logs,
            "page": page,
            "total_pages": total_pages,
            "total_logs": total_logs,
        },
    )

@router.post("/scheduler/run")
def run_pipeline():

    if state.scheduler is None:

        return RedirectResponse(
            "/scheduler",
            status_code=303,
        )

    state.scheduler.run_pipeline()

    return RedirectResponse(
        "/scheduler",
        status_code=303,
    )

@router.post("/scheduler/pause")
def pause_scheduler():

    if state.scheduler is not None:

        state.scheduler.pause()

    return RedirectResponse(
        "/scheduler",
        status_code=303,
    )


@router.post("/scheduler/resume")
def resume_scheduler():

    if state.scheduler is not None:

        state.scheduler.resume()

    return RedirectResponse(
        "/scheduler",
        status_code=303,
    )