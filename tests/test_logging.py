"""Tests for logging utilities."""

import logging
from pathlib import Path
import tempfile
from horizon_core.logging import setup_logging, get_logger, LoggerMixin


def test_setup_logging_basic():
    """Test basic logging setup."""
    setup_logging(level="INFO")
    logger = get_logger(__name__)
    assert logger.level <= logging.INFO


def test_setup_logging_with_file():
    """Test logging setup with file output."""
    with tempfile.TemporaryDirectory() as tmpdir:
        log_file = Path(tmpdir) / "test.log"
        setup_logging(level="DEBUG", log_file=log_file)

        logger = get_logger(__name__)
        logger.info("Test message")

        assert log_file.exists()
        content = log_file.read_text()
        assert "Test message" in content


def test_get_logger():
    """Test getting a logger instance."""
    logger = get_logger("test.module")
    assert isinstance(logger, logging.Logger)
    assert logger.name == "test.module"


def test_logger_mixin():
    """Test LoggerMixin class."""

    class TestClass(LoggerMixin):
        pass

    obj = TestClass()
    logger = obj.logger
    assert isinstance(logger, logging.Logger)
    assert logger.name == "TestClass"


def test_simple_format():
    """Test simple logging format."""
    setup_logging(level="INFO", simple=True)
    logger = get_logger(__name__)
    # Just verify it doesn't raise an error
    logger.info("Test message")
