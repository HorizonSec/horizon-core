# Horizon Core

[![Full Build](https://github.com/HorizonSec/horizon-core/workflows/Full%20Build/badge.svg)](https://github.com/HorizonSec/horizon-core/actions)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

## Overview

Welcome to the **Horizon Core** repository! This is the core library providing shared utilities and framework components for the HorizonSec organization, including secure logging with automatic sensitive data redaction and a standardized CLI framework for building consistent command-line tools.

This repository includes:
- **CLI Framework**: Standardized command-line interface framework with rich styling and interactive features
- **SecureLogger**: A logging system that automatically redacts sensitive information
- **SensitiveDataFormatter**: A formatter that prevents sensitive data leaks in logs  
- **Configuration Management**: Utilities for handling application configuration
- **SARIF Support**: Schema definitions for Static Analysis Results Interchange Format
- Comprehensive documentation (README, CONTRIBUTING, CODE_OF_CONDUCT)
- Issue and pull request templates
- GitHub Actions workflows for building, testing, and documentation
- Security policy and vulnerability scanning
- Standard .gitignore configurations
- Open-source license (MIT)

## Getting Started

### Prerequisites

Before using Horizon Core, ensure you have:
- Python 3.9 or higher
- pip (Python package installer)
- Git installed on your local machine

### Installation

1. **Clone the repository**:
   ```bash
   git clone https://github.com/HorizonSec/horizon-core.git
   cd horizon-core
   ```

2. **Install using Hatch** (recommended):
   ```bash
   pip install hatch
   hatch shell
   ```

3. **Or install directly**:
   ```bash
   pip install -e .
   ```

4. **For development with all tools**:
   ```bash
   pip install hatch
   hatch env create dev
   hatch shell dev
   ```

### Quick Start

#### Secure Logging

```python
from horizon_core import setup_logger
import logging

# Set up a secure logger that automatically redacts sensitive information
logger = setup_logger("my-app", level=logging.INFO)

# These messages will have sensitive data automatically redacted
logger.info("Starting application")
logger.info("User password is secret123")  # Will show: "User password is [REDACTED]"
logger.info("API key: abc123def456")        # Will show: "API key: [REDACTED]"
```

#### CLI Framework

```python
from horizon_core.cli_wrapper import CLI

# Create a CLI application with consistent styling
cli = CLI("MyTool", "A security analysis tool", "1.0.0")

# Add commands with decorators
@cli.add_command
def scan():
    """Run security scan."""
    print("Running scan...")

# Run the CLI with built-in help, version, and interactive mode
if __name__ == "__main__":
    cli.run()
```

## Usage

Horizon Core provides two main components: secure logging utilities and a CLI framework for building consistent command-line applications.

### CLI Framework

The CLI framework provides a standardized way to build command-line tools with consistent styling, interactive features, and rich console output.

#### Basic CLI Application

```python
from horizon_core.cli_wrapper import CLI
import typer

# Create a CLI with automatic help, version, and interactive mode
cli = CLI("SecurityTool", "Advanced security analysis", "2.0.0")

# Add commands using decorators
@cli.add_command
def scan(target: str = typer.Argument(..., help="Target to scan")):
    """Scan target for vulnerabilities."""
    print(f"Scanning {target}...")

@cli.add_command  
def report(format: str = typer.Option("json", help="Report format")):
    """Generate security report."""
    print(f"Generating {format} report...")

# Built-in commands available: --help, version, interactive
if __name__ == "__main__":
    cli.run()
```

#### Interactive Mode

```python
# Register interactive commands for guided usage
def run_full_scan():
    """Run comprehensive security scan."""
    print("Starting full security scan...")
    
def view_last_results():
    """View results from last scan."""
    print("Displaying scan results...")

cli.register_interactive_command("full-scan", run_full_scan)
cli.register_interactive_command("results", view_last_results)

# Users can now run: python tool.py interactive
```

#### Command Groups

```python
# Create organized command groups
scan_group = cli.add_group("scan", "Scanning operations")
report_group = cli.add_group("report", "Reporting operations")

@scan_group.command()
def network():
    """Scan network infrastructure."""
    print("Network scan starting...")

@report_group.command()
def generate():
    """Generate detailed report."""
    print("Report generation starting...")
```

### Secure Logging

The main feature of Horizon Core is the `SecureLogger` that automatically redacts sensitive information from log messages:

```python
from horizon_core import setup_logger
import logging

# Create a secure logger
logger = setup_logger("myapp", level=logging.INFO)

# Log normally - sensitive data will be automatically redacted
logger.info("Database connection: postgresql://user:password@localhost/db")
logger.warning("Invalid API token: secret123token")
logger.error("Authentication failed for key=abc123")

# Output will show:
# INFO: Database connection: postgresql://user:[REDACTED]@localhost/db
# WARNING: Invalid API token: [REDACTED]
# ERROR: Authentication failed for key=[REDACTED]
```

#### Sensitive Data Patterns

The logger automatically detects and redacts the following sensitive patterns:
- Passwords (`password is secret`, `password=value`, `password: value`)
- API keys (`api_key: value`, `apikey=value`)
- Tokens (`token: value`, `token=value`)
- Authorization headers (`authorization: bearer`, `auth=value`)
- Credentials, secrets, private keys, sessions, cookies, JWT tokens, OAuth tokens

#### Simple vs Detailed Logging Format

```python
# Detailed format (default): includes timestamp, logger name, level
logger = setup_logger("myapp", level=logging.INFO, simple=False)
# Output: 2024-01-01 12:00:00,000 - myapp - INFO - Application started

# Simple format: just level and message
logger = setup_logger("myapp", level=logging.INFO, simple=True)
# Output: INFO: Application started
```

#### Custom Logger Configuration

```python
from horizon_core.logger import SecureLogger, SensitiveDataFormatter
import logging

# Create a custom secure logger with your own configuration
logger = SecureLogger("custom-app")
logger.setLevel(logging.DEBUG)

# Add custom handler with sensitive data formatting
handler = logging.StreamHandler()
formatter = SensitiveDataFormatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
handler.setFormatter(formatter)
logger.addHandler(handler)

# Use the logger
logger.debug("Debug info with secret=hidden_value")
```

### Development

#### Using Hatch

This project uses [Hatch](https://hatch.pypa.io/) for dependency management and development tasks.

Run tests:
```bash
hatch run test
```

Run tests with coverage:
```bash
hatch run test-cov
hatch run cov-report
```

Format code:
```bash
hatch run format
```

Check code quality:
```bash
hatch run pre-build
```

Build documentation:
```bash
hatch run dev:docs
```

Build the package:
```bash
hatch build
```

#### Development Environment

Set up development environment:
```bash
hatch env create dev
hatch shell dev
```

Run type checking:
```bash
hatch run dev:typecheck
```

Run security checks:
```bash
hatch run dev:bandit -r ./horizon_core
```

### Project Structure

See [FOLDER_STRUCTURE.md](FOLDER_STRUCTURE.md) for a detailed explanation of the repository structure.

### CI/CD Pipeline

The project uses multiple GitHub Actions workflows:

#### Full Build (`.github/workflows/full-build.yml`)
Runs on every push and includes:
- Building across Python 3.9-3.13
- Linting with black, isort, flake8
- Type checking with mypy
- Unit testing with pytest
- Package building with hatch

#### Security Scanning (`.github/workflows/security-scanning.yml`)
Runs after successful builds on the mainline branch:
- Bandit security scanning
- Vulnerability detection
- Security report generation

#### Documentation (`.github/workflows/docs.yml`)
Builds and deploys documentation:
- Builds Sphinx documentation
- Deploys to GitHub Pages
- Runs on mainline branch pushes

## Contributing

We welcome contributions from the community! Please read our [CONTRIBUTING.md](CONTRIBUTING.md) for details on:
- How to submit issues
- How to create pull requests
- Coding standards and best practices
- Development workflow

## Code of Conduct

This project adheres to a Code of Conduct that all contributors are expected to follow. Please read [CODE_OF_CONDUCT.md](CODE_OF_CONDUCT.md) to understand the expected behavior when participating in this project.

## Security

If you discover a security vulnerability, please follow the guidelines in [SECURITY.md](SECURITY.md) to report it responsibly.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Support

For questions, issues, or feature requests:
- Open an issue using the appropriate template
- Contact the HorizonSec team
- Check existing documentation and issues

## Acknowledgments

- Thanks to all contributors who help improve Horizon Core
- Built with ❤️ by the HorizonSec team