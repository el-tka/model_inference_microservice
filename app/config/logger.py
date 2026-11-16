"""
This module contains the configuration settings for the logging.
It defines the LoggerSettings class, which uses Pydantic to manage
configuration settings, allowing settings to be read from environment
variables and .env file.
"""

from pathlib import Path
import sys

from loguru import logger
from pydantic_settings import BaseSettings, SettingsConfigDict


CONFIG_DIR = Path(__file__).resolve().parent
BASE_DIR = CONFIG_DIR.parent.parent

LOG_DIR = BASE_DIR / "logs"
LOG_DIR.mkdir(parents=True, exist_ok=True)


class LoggerSettings(BaseSettings):
    """
    Configuration settings for the logging.

    Attributes:
        model_config (SettingsConfigDict): Configuration for reading settings
        from a .env file.
        log_level (str): Logging level for the application.
    """

    model_config = SettingsConfigDict(
        env_file=CONFIG_DIR / ".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )

    log_level: str = "INFO"


def configure_logging(log_level: str) -> None:
    """
    Configures the logging settings for the application.

    Args:
        log_level (str): The logging level to be set for the application.

    Returns:
        None
    """
    logger.remove()

    logger.add(
        sys.stderr,
        level=log_level,
        format=(
            "{time:YYYY-MM-DD HH:mm:ss} | "
            "{level} | {name}:{function}:{line} | "
            "{message}"
        ),
    )

    logger.add(
        LOG_DIR / "app.log",
        rotation="10 MB",
        retention="7 days",
        compression="zip",
        level=log_level,
        enqueue=True,
    )


# Configure logging
configure_logging(LoggerSettings().log_level)
