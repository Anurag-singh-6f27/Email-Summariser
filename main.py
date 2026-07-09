"""
Application entry point for the Personal AI Email Summarizer.

Responsibilities:
- Initialize logging
- Load application configuration
- Verify environment variables
- Start the application
"""

from __future__ import annotations

import sys

from config import load_config
from utils.logger import get_logger, setup_logger


def main() -> None:
    """
    Main application entry point.
    """
    print("Loading configuration...")

    # Initialize logging first
    setup_logger()
    logger = get_logger()

    logger.info("Logger initialized.")

    try:
        config = load_config()

        logger.info("Environment variables loaded successfully.")
        logger.info(
            f"Configured email accounts: {len(config.email_accounts)}"
        )
        logger.info("Application started successfully.")

        print("Application started successfully.")

    except Exception as exc:
        logger.exception("Application failed to start.")
        print(f"\nStartup Error: {exc}")
        sys.exit(1)


if __name__ == "__main__":
    main()