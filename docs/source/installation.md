# Installation

## Requirements

- Python 3.9 or higher
- pip (Python package installer)

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

To verify the installation:

```python
from horizon_core import setup_logger
logger = setup_logger("test")
logger.info("Installation successful!")
```

If no errors occur, the installation was successful.