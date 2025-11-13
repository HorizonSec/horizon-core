# Configuration

This directory is reserved for future configuration files for Horizon Core.

Currently, Horizon Core focuses on secure logging and does not require external configuration files. All configuration is done programmatically through the `setup_logger()` function.

## Future Structure

As the project expands, configuration may be organized into:

- **logging/**: Logging-specific configuration files
- **development/**: Development environment settings
- **production/**: Production environment settings

## Current Logging Configuration

Horizon Core's secure logging is configured programmatically:

```python
from horizon_core import setup_logger
import logging

# Basic configuration
logger = setup_logger("my-app", level=logging.INFO)

# Simple format (just level and message)
logger = setup_logger("my-app", level=logging.INFO, simple=True)

# Custom configuration
from horizon_core.logging import SecureLogger, SensitiveDataFormatter

logger = SecureLogger("custom-app")
handler = logging.StreamHandler()
formatter = SensitiveDataFormatter("%(asctime)s - %(levelname)s - %(message)s")
handler.setFormatter(formatter)
logger.addHandler(handler)
```

## Current Config
This module provides a lightweight and extensible configuration loader for user-defined settings.  
It reads a local JSON file (default: `horizon_config.json`) and converts it into structured Python objects for easy access and validation.

- Loads user configuration from `horizon_config.json` in the current directory.  
- Uses Python `dataclasses` to map configuration sections into structured objects.  
- Automatically applies safe defaults when fields or files are missing.  
- Can optionally load configurations from a custom path.  
- Simple and dependency-free — based entirely on the Python standard library.

# Example Configuration File
Create a file named `horizon_config.json` in your current working directory:

```json
{
  "risk_appetite": {
    "level": "medium",
    "max_investment_per_asset": 5000,
    "stop_loss_threshold": 0.1
  },
  "rules": {
    "enable_email_alerts": true,
    "enable_sms_alerts": false,
    "allow_margin_trading": false
  },
  "opt_in_features": ["daily_summary", "portfolio_rebalancing"]
}

## Security Best Practices

1. **No secrets in logs**: Horizon Core automatically redacts sensitive data
2. **Use secure loggers**: Always use `setup_logger()` or `SecureLogger` 
3. **Review log output**: Test that sensitive data is properly redacted
4. **Custom patterns**: Add custom sensitive patterns if needed
5. **Log levels**: Use appropriate log levels to avoid over-logging

## Questions?

If you have questions about configuration:
- Check the [CONTRIBUTING.md](../CONTRIBUTING.md) for guidelines
- Review existing configuration for examples
- Open an issue for discussion
