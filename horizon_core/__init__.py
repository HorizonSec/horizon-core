"""
Horizon Core - Shared utilities and framework for HorizonSec tools.

This package provides common functionality including:
- CLI framework for building command-line tools
- Logging utilities for consistent logging across tools
- SARIF schema definitions for security findings
- Configuration management utilities
"""

__version__ = "0.1.0"
__author__ = "HorizonSec Team"


from .logging import setup_logger

__all__ = [
    "setup_logger",
    "__version__",
]
