"""
Application entry point.

Starts the scheduler and keeps the application
running until shutdown.
"""

from __future__ import annotations

import sys

from config import load_config

from scheduler import Scheduler

from utils.logger import (
    get_logger,
    setup_logger,
)


def main() -> None:
    """
    Application entry point.
    """

    setup_logger()

    logger = get_logger()

    logger.info("=" * 60)
    logger.info("Starting Personal AI Email Summarizer")
    logger.info("=" * 60)

    scheduler = None

    try:

        logger.info(
            "Loading configuration..."
        )

        config = load_config()

        logger.info(
            "Loaded {} configured email account(s).",
            len(config.email_accounts),
        )

        scheduler = Scheduler(
            config
        )

        scheduler.start()

        scheduler.wait_forever()

    except KeyboardInterrupt:

        logger.info(
            "Shutdown requested by user."
        )

    except Exception:

        logger.exception(
            "Application terminated unexpectedly."
        )

        sys.exit(1)

    finally:

        if scheduler is not None:

            scheduler.shutdown()

        logger.info("=" * 60)
        logger.info("Application stopped.")
        logger.info("=" * 60)


if __name__ == "__main__":

    main()