"""A utility module for logging configuration."""

import os
import logging

log_level = os.getenv("LOG_LEVEL", "INFO").upper()
log_format = os.getenv(
    "LOG_FORMAT", "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
numerical_log_level = getattr(logging, log_level, logging.INFO)
if not isinstance(numerical_log_level, int):
    raise ValueError(f"Invalid log level: {log_level}")
logging.basicConfig(
    level=numerical_log_level,
    format=log_format,
)


def get_logger(name: str) -> logging.Logger:
    """
    Get a logger with the specified name.

    Args:
        name (str): The name of the logger.

    Returns:
        logging.Logger: The logger instance.
    """
    return logging.getLogger(name)
