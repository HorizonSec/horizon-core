# Horizon Core Documentation

Welcome to the **Horizon Core** documentation! This library provides shared utilities and framework components for HorizonSec tools, including secure logging with automatic sensitive data redaction and a standardized CLI framework.

Quick Start
-----------

### Secure Logging

.. code-block:: python

   from horizon_core import setup_logger
   import logging

   # Create a secure logger with automatic sensitive data redaction
   logger = setup_logger("myapp", level=logging.INFO)

   # Log messages - sensitive data will be automatically redacted
   logger.info("Starting application")
   logger.info("User password is secret123")  # Output: "User password is [REDACTED]"
   logger.info("API key: abc123def456")        # Output: "API key: [REDACTED]"

### CLI Framework

.. code-block:: python

   from horizon_core.cli_wrapper import CLI

   # Create a CLI application
   cli = CLI("MyTool", "A security analysis tool", "1.0.0")

   # Add custom commands
   @cli.add_command
   def scan():
       """Run security scan."""
       print("Running scan...")

   # Run the CLI
   if __name__ == "__main__":
       cli.run()

Key Features
------------

- **Secure Logging**: Automatic redaction of passwords, API keys, tokens, and other sensitive data
- **CLI Framework**: Standardized command-line interface with consistent styling and interactive mode
- **Rich Console Output**: Beautiful, styled console output with colors and formatting
- **Interactive Mode**: Guided menu-driven interface for improved usability
- **Security First**: Built-in protections to prevent sensitive information leaks
- **Easy Integration**: Drop-in components for rapid tool development
- **Performance Optimized**: Minimal overhead with efficient implementations

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