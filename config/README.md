# Configuration

This directory contains configuration files for Horizon Core.

## Structure

As the project develops, configuration will be organized into:

- **development/**: Development environment configuration
- **staging/**: Staging environment configuration  
- **production/**: Production environment configuration
- Tool-specific configuration files

## Configuration Guidelines

When adding configuration:

1. **Use environment variables**: Keep sensitive data out of configuration files
2. **Provide defaults**: Include sensible default values
3. **Document options**: Comment configuration options clearly
4. **Separate by environment**: Use different configs for different environments
5. **Version control**: Commit configuration files (but not secrets!)

## Environment Variables

Sensitive configuration should be stored in environment variables, not in files committed to the repository.

Example `.env` file structure (do not commit):
```
# Database configuration
DB_HOST=localhost
DB_PORT=5432
DB_NAME=horizon_core
DB_USER=your_user
DB_PASSWORD=your_password

# API keys (never commit these!)
API_KEY=your_api_key_here
SECRET_KEY=your_secret_key_here
```

## Configuration Best Practices

1. **Never commit secrets**: Use `.gitignore` to exclude files with sensitive data
2. **Use a .env.example file**: Provide a template with placeholder values
3. **Document all options**: Include comments explaining what each setting does
4. **Validate configuration**: Check that required values are present at startup
5. **Use type-safe configs**: Validate configuration types when possible

## Questions?

If you have questions about configuration:
- Check the [CONTRIBUTING.md](../CONTRIBUTING.md) for guidelines
- Review existing configuration for examples
- Open an issue for discussion
