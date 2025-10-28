# Horizon Core Documentation

Welcome to the **Horizon Core** documentation! This library provides secure logging utilities with automatic sensitive data redaction for HorizonSec tools.

Quick Start
-----------

.. code-block:: python

   from horizon_core import setup_logger
   import logging

   # Create a secure logger with automatic sensitive data redaction
   logger = setup_logger("myapp", level=logging.INFO)

   # Log messages - sensitive data will be automatically redacted
   logger.info("Starting application")
   logger.info("User password is secret123")  # Output: "User password is [REDACTED]"
   logger.info("API key: abc123def456")        # Output: "API key: [REDACTED]"

Key Features
------------

- **Automatic Redaction**: Detects and redacts passwords, API keys, tokens, and other sensitive data
- **Security First**: Prevents sensitive information leaks in log files
- **Easy Integration**: Drop-in replacement for standard Python logging
- **Performance Optimized**: Minimal overhead with optional simple format mode
- **Robust Error Handling**: Graceful handling of malformed log messages

Table of Contents
-----------------

.. toctree::
   :maxdepth: 2
   :caption: Contents:

   installation
   api
   examples
   security

Indices and tables
------------------

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`