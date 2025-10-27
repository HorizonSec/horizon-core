# Documentation

This directory contains the Sphinx documentation for Horizon Core, a secure logging library that provides automatic redaction of sensitive information from log messages.

## Structure

- **source/**: Sphinx source files (.rst and .md files)
  - `index.rst`: Main documentation index
  - `installation.md`: Installation instructions
  - `api.md`: API reference documentation  
  - `examples.md`: Usage examples and code samples
  - `security.md`: Security considerations and best practices
  - `conf.py`: Sphinx configuration
- **build/**: Generated HTML documentation (created when building)

## Building Documentation

To build the documentation locally:

```bash
# Install dependencies (if not already done)
pip install hatch

# Build documentation
hatch run dev:docs

# Clean build (rebuild everything)
hatch run dev:docs-clean

# Serve documentation locally
hatch run dev:docs-serve
```

The generated HTML documentation will be in `docs/build/` and can be viewed by opening `docs/build/index.html` in a web browser.

## Documentation Guidelines

When writing documentation:

1. **Be clear and concise**: Use simple language and avoid jargon when possible
2. **Provide examples**: Include code examples and use cases
3. **Keep it updated**: Update documentation when code changes
4. **Use proper formatting**: Follow markdown best practices
5. **Link related content**: Cross-reference related documentation

## Documentation Index

This section will contain links to key documentation as it's added:

## Documentation Content

### Getting Started
- **Installation Guide**: Complete installation instructions for different environments
- **Quick Start Guide**: Basic usage examples to get started immediately

### API Documentation
- **SecureLogger**: Full API reference for the secure logger class
- **SensitiveDataFormatter**: Documentation for the redaction formatter
- **setup_logger**: Function reference for creating secure loggers

### Usage Guides  
- **Examples**: Comprehensive usage examples for various scenarios
- **Security Best Practices**: Guidelines for secure logging implementation
- **Integration Patterns**: How to integrate with existing applications

### Security Documentation
- **Threat Model**: Understanding the security risks addressed
- **Redaction Patterns**: Details on what sensitive data is detected
- **Deployment Guidelines**: Secure deployment and configuration practices

## Contributing to Documentation

Documentation contributions are welcome! To contribute:

1. Follow the [CONTRIBUTING.md](../CONTRIBUTING.md) guidelines
2. Use clear, concise language
3. Include examples where appropriate
4. Ensure proper markdown formatting
5. Submit a pull request

## Questions?

If you have questions about documentation:
- Check existing documentation for examples
- Review the [CONTRIBUTING.md](../CONTRIBUTING.md) guidelines
- Open an issue for discussion
