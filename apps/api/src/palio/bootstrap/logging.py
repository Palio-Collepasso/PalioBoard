"""Loguru configuration helpers."""

import logging
import sys

from loguru import logger

from palio.settings import LoggingSettings


def configure_logging(settings: LoggingSettings) -> None:
    """Configure Loguru for JSON output."""
    logger.remove()
    logger.add(
        sys.stdout,
        level=settings.level.value,
        serialize=True,
        backtrace=False,
        diagnose=False,
    )
    logging.getLogger("uvicorn.access").disabled = True
