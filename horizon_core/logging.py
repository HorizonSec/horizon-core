"""
Logging utilities - Standardized logging configuration.

This module provides consistent logging setup across HorizonSec tools.
"""

import logging
import sys
from pathlib import Path
from typing import Optional


# Default log format
DEFAULT_FORMAT = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
SIMPLE_FORMAT = "%(levelname)s: %(message)s"


def setup_logging(
    level: str = "INFO",
    log_file: Optional[Path] = None,
    format_string: Optional[str] = None,
    simple: bool = False,
) -> None:
    """
    Set up logging configuration.

    Args:
        level: Logging level (DEBUG, INFO, WARNING, ERROR, CRITICAL)
        log_file: Optional file path to write logs to
        format_string: Custom format string for log messages
        simple: Use simple format (just level and message)
    """
    # Determine format
    if format_string is None:
        format_string = SIMPLE_FORMAT if simple else DEFAULT_FORMAT

    # Convert level string to logging constant
    numeric_level = getattr(logging, level.upper(), None)
    if not isinstance(numeric_level, int):
        raise ValueError(f"Invalid log level: {level}")

    # Configure root logger
    handlers = []

    # Console handler
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(numeric_level)
    console_handler.setFormatter(logging.Formatter(format_string))
    handlers.append(console_handler)

    # File handler (if specified)
    if log_file:
        log_file.parent.mkdir(parents=True, exist_ok=True)
        file_handler = logging.FileHandler(log_file)
        file_handler.setLevel(numeric_level)
        file_handler.setFormatter(logging.Formatter(DEFAULT_FORMAT))
        handlers.append(file_handler)

    # Apply configuration
    logging.basicConfig(
        level=numeric_level,
        format=format_string,
        handlers=handlers,
        force=True,
    )


def get_logger(name: str) -> logging.Logger:
    """
    Get a logger instance.

    Args:
        name: Logger name (typically __name__ of the calling module)

    Returns:
        Logger instance
    """
    return logging.getLogger(name)


class LoggerMixin:
    """Mixin class to add logging capabilities to any class."""

    @property
    def logger(self) -> logging.Logger:
        """Get a logger for this class."""
        return get_logger(self.__class__.__name__)
