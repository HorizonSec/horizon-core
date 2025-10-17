# Horizon Core

[![CI](https://github.com/HorizonSec/horizon-core/workflows/CI/badge.svg)](https://github.com/HorizonSec/horizon-core/actions)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

## Overview

Welcome to the **Horizon Core** repository! This is the core library and framework for the HorizonSec organization, providing fundamental components, utilities, and services for building secure applications.

This repository includes:
- Comprehensive documentation (README, CONTRIBUTING, CODE_OF_CONDUCT)
- Issue and pull request templates
- GitHub Actions CI workflow
- Security policy
- Standard .gitignore configurations
- Open-source license (MIT)

## Getting Started

### Prerequisites

Before using Horizon Core, ensure you have:
- Python 3.8 or higher
- pip (Python package installer)
- Git installed on your local machine

### Installation

1. **Clone the repository**:
   ```bash
   git clone https://github.com/HorizonSec/horizon-core.git
   cd horizon-core
   ```

2. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Install the package** (development mode):
   ```bash
   pip install -e .
   ```

   Or using Hatch:
   ```bash
   pip install hatch
   hatch shell
   ```

### Quick Start

```python
from horizon_core import CLI, Command, setup_logging, get_logger

# Set up logging
setup_logging(level="INFO")
logger = get_logger(__name__)

# Use the CLI framework
# (See examples in docs/)
```

## Usage

Horizon Core provides shared utilities and framework for building security tools. Here's how to use it:

### Core Modules

#### CLI Framework
Build command-line tools with a standardized interface:

```python
from horizon_core import CLI, Command
import argparse

class MyCommand(Command):
    def __init__(self):
        super().__init__("scan", "Scan for security issues")
    
    def configure_parser(self, parser: argparse.ArgumentParser):
        parser.add_argument("--target", required=True, help="Target to scan")
    
    def execute(self, args: argparse.Namespace) -> int:
        print(f"Scanning {args.target}...")
        return 0

cli = CLI("mytool", "My Security Tool", "1.0.0")
cli.add_command(MyCommand())
cli.run()
```

#### Logging
Consistent logging across tools:

```python
from horizon_core import setup_logging, get_logger

setup_logging(level="INFO")
logger = get_logger(__name__)
logger.info("Application started")
```

#### SARIF Output
Generate standardized security findings in SARIF format:

```python
from horizon_core.sarif import SARIFReport, Run, Tool, Result, Message

report = SARIFReport()
tool = Tool(name="MyScanner", version="1.0.0")
run = Run(tool=tool)
run.results.append(Result(
    ruleId="SEC001",
    message=Message(text="Security issue found")
))
report.add_run(run)
report.save("results.sarif")
```

#### Configuration Management
Load and manage configuration from files and environment:

```python
from horizon_core import load_config

config = load_config("config.yaml")
port = config.get("server.port", 8080)
```

### Development

Run tests:
```bash
hatch run test
```

Run tests with coverage:
```bash
hatch run test-cov
```

Format code:
```bash
hatch run lint:format
```

Check code quality:
```bash
hatch run lint:check
```

### Docker

Build the Docker image:
```bash
docker build -t horizon-core .
```

Run in Docker:
```bash
docker run -it horizon-core python -c "import horizon_core; print(horizon_core.__version__)"
```

### Project Structure

See [FOLDER_STRUCTURE.md](FOLDER_STRUCTURE.md) for a detailed explanation of the repository structure.

### Running CI

The GitHub Actions workflow (`.github/workflows/ci.yml`) automatically runs on:
- Push to main branch
- Pull requests to main branch

The workflow includes:
- Linting with black, isort, flake8, and mypy
- Testing across Python 3.8-3.12
- Security checks
- Package building

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