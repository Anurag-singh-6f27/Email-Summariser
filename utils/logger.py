"""
Application logging configuration.

This module configures Loguru for:
- Console logging
- File logging
- Daily log rotation
- Log retention
- Log compression
"""

from __future__ import annotations

import sys
from pathlib import Path

from loguru import logger


LOG_DIRECTORY = Path("logs")
LOG_DIRECTORY.mkdir(exist_ok=True)


def setup_logger() -> None:
    """
    Configure the application logger.

    This function should be called once during application startup.
    """

    # Remove Loguru's default logger
    logger.remove()

    # Console Logger
    logger.add(
        sys.stdout,
        level="INFO",
        colorize=True,
        format=(
            "<green>{time:YYYY-MM-DD HH:mm:ss}</green> | "
            "<level>{level:<8}</level> | "
            "<cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> | "
            "<level>{message}</level>"
        ),
    )

    # File Logger
    LOG_DIRECTORY.mkdir(parents=True, exist_ok=True)
    logger.add(
        LOG_DIRECTORY / "application.log",
        level="DEBUG",
        rotation="00:00",      # Rotate every day at midnight
        retention="30 days",   # Keep logs for 30 days
        compression="zip",     # Compress old logs
        encoding="utf-8",
        enqueue=True,
        backtrace=True,
        diagnose=True,
        format=(
            "{time:YYYY-MM-DD HH:mm:ss} | "
            "{level:<8} | "
            "{name}:{function}:{line} | "
            "{message}"
        ),
    )


def get_logger():
    """
    Return the configured Loguru logger.

    Returns:
        loguru.Logger: Shared logger instance.
    """
    return logger