# Installation

## Requirements

- Python 3.9 or higher
- pip (Python package installer)

## Dependencies

Horizon Core includes the following dependencies:

- **typer**: Modern CLI framework for building command-line interfaces
- **rich**: Rich text and beautiful formatting in the terminal
- **pyfiglet**: ASCII art text generation for CLI banners
- **pyyaml**: YAML configuration file support

## Installation Methods

### Using Hatch (Recommended)

If you're developing with the project:

```bash
git clone https://github.com/HorizonSec/horizon-core.git
cd horizon-core
pip install hatch
hatch shell
```

### Direct Installation

For production use:

```bash
pip install horizon-core
```

### Development Installation

For contributing to the project:

```bash
git clone https://github.com/HorizonSec/horizon-core.git
cd horizon-core
pip install hatch
hatch env create dev
hatch shell dev
```

## Verification

### Test Secure Logging

To verify the logging functionality:

```python
from horizon_core import setup_logger
logger = setup_logger("test")
logger.info("Installation successful!")
logger.info("Testing redaction - password is secret123")
```

### Test CLI Framework

To verify the CLI framework:

```python
from horizon_core.cli_wrapper import CLI

cli = CLI("TestApp", "Testing CLI installation", "1.0.0")

@cli.add_command
def hello():
    """Test command."""
    print("Hello from Horizon Core CLI!")

if __name__ == "__main__":
    cli.run()
```

Save this as `test_cli.py` and run:

```bash
python test_cli.py hello
python test_cli.py --help
python test_cli.py interactive
```

If no errors occur, the installation was successful.