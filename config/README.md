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
