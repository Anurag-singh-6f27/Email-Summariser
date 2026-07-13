"""
Application scheduler.

Responsible for scheduling and triggering
pipeline execution.
"""

from __future__ import annotations

import signal
import threading
import time

from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.cron import CronTrigger

from config import AppConfig
from pipeline import Pipeline

from utils.logger import get_logger

logger = get_logger()


class Scheduler:
    """
    Coordinates scheduled pipeline execution.
    """

    def __init__(
        self,
        config: AppConfig,
    ) -> None:

        self._config = config

        self._pipeline = Pipeline(
            config
        )

        self._scheduler = BackgroundScheduler(
            timezone=config.scheduler.timezone
        )

        self._lock = threading.Lock()

        self._running = False

    def _execute_pipeline(
        self,
    ) -> None:

        if not self._lock.acquire(
            blocking=False,
        ):

            logger.warning(
                "Pipeline execution skipped because another execution is already running."
            )

            return

        self._running = True

        logger.info(
            "Pipeline job triggered."
        )

        try:

            statistics = self._pipeline.run()

            logger.info(
                "Pipeline completed successfully."
            )

            logger.info(
                "Duration: {:.2f} seconds.",
                statistics.duration_seconds,
            )

            logger.info(
                "Fetched: {} | Summaries: {} | Telegram: {} | Errors: {}",
                statistics.emails_fetched,
                statistics.summaries_generated,
                statistics.telegram_messages_sent,
                statistics.errors,
            )

        except Exception:

            logger.exception(
                "Unhandled pipeline exception."
            )

        finally:

            self._running = False

            self._lock.release()


    def run_pipeline(
        self,
    ) -> None:
        """
        Execute the pipeline immediately.
        """

        self._execute_pipeline()



    def start(
        self,
    ) -> None:

        if not self._config.scheduler.enabled:

            logger.warning(
                "Scheduler is disabled."
            )

            return

        trigger = CronTrigger(

            hour=self._config.scheduler.hour,

            minute=self._config.scheduler.minute,

            timezone=self._config.scheduler.timezone,
        )

        self._scheduler.add_job(

            func=self._execute_pipeline,

            trigger=trigger,

            id="email_pipeline",

            replace_existing=True,

            max_instances=1,

            coalesce=True,

            misfire_grace_time=300,
        )

        self._scheduler.start()

        logger.info(
            "Scheduler started."
        )

        logger.info(
            "Schedule: hour='{}' minute='{}' timezone='{}'.",
            self._config.scheduler.hour,
            self._config.scheduler.minute,
            self._config.scheduler.timezone,
        )

        if self._config.scheduler.run_on_startup:

            logger.info(
                "Executing startup pipeline."
            )

            self._execute_pipeline()

    def shutdown(
        self,
    ) -> None:

        logger.info(
            "Stopping scheduler."
        )

        if self._scheduler.running:

            self._scheduler.shutdown(
                wait=True
            )
        self._pipeline.close()

        logger.info(
            "Scheduler stopped."
        )

    def wait_forever(
        self,
    ) -> None:

        def _signal_handler(
            signum,
            frame,
        ) -> None:

            logger.info(
                "Shutdown signal received."
            )

            raise KeyboardInterrupt

        signal.signal(
            signal.SIGINT,
            _signal_handler,
        )

        signal.signal(
            signal.SIGTERM,
            _signal_handler,
        )

        logger.info(
            "Scheduler is running."
        )

        while True:

            time.sleep(1)

    def pause(
        self,
    ) -> None:
        """
        Pause scheduled pipeline executions.
        """

        self._scheduler.pause()
        logger.info(
        "Scheduler paused."
        )

    def resume(
        self,
    ) -> None:
        """
        Resume scheduled pipeline executions.
        """

        self._scheduler.resume()
        logger.info(
        "Scheduler resumed."
        )

    def is_running(
        self,
    ) -> bool:
        """
        Return whether the scheduler is running.
        """

        return self._scheduler.running