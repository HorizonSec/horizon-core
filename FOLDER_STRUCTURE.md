# Folder Structure

This document describes the organization and structure of the Horizon Core repository. Understanding this structure will help you navigate the codebase and know where to place new files.

## Repository Structure

```
horizon-core/
├── .github/                          # GitHub-specific configurations
│   ├── ISSUE_TEMPLATE/              # Issue templates for bug reports and feature requests
│   │   ├── bug_report.md           # Template for reporting bugs
│   │   └── feature_request.md      # Template for requesting features
│   ├── workflows/                   # GitHub Actions workflows
│   │   ├── docs.yml                # Documentation build and deployment
│   │   ├── full-build.yml          # Full build pipeline with testing
│   │   └── security-scanning.yml   # Security scanning workflow
│   └── PULL_REQUEST_TEMPLATE.md    # Template for pull requests
├── config/                          # Configuration files
│   └── README.md                   # Configuration documentation
├── docs/                            # Additional documentation
│   └── README.md                   # Documentation index
├── horizon_core/                    # Main Python package
│   ├── __init__.py                 # Package initialization (exports setup_logger)
│   ├── cli_framework.py            # Empty file (functionality removed)
│   ├── logging.py                  # Secure logging utilities with data redaction
│   ├── sarif.py                    # Empty file (functionality removed)
│   └── config.py                   # Empty file (functionality removed)
├── tests/                           # Unit and integration tests
│   ├── __init__.py
│   ├── test_cli_framework.py       # Empty file (tests removed)
│   ├── test_logging.py             # Comprehensive tests for logging module
│   ├── test_sarif.py               # Empty file (tests removed)
│   └── test_config.py              # Empty file (tests removed)
├── tests-resources/                # Unit tests resources
│  ├─ empty_file.json
│  ├─ features_only.json
│  ├─ full_config.json
│  ├─ invalid_json_syntax.json
│  ├─ invalid_unexpected_fields.json
│  ├─ partial_config.json
│  └─ wrong_data_types.json
├── .gitignore                       # Git ignore patterns
├── CODE_OF_CONDUCT.md               # Community code of conduct
├── CONTRIBUTING.md                  # Contribution guidelines
├── FOLDER_STRUCTURE.md              # This file - describes repository structure
├── LICENSE                          # MIT License
├── pyproject.toml                   # Python project configuration (Hatch)
├── README.md                        # Main project documentation
├── requirements.txt                 # Python dependencies
└── SECURITY.md                      # Security policy and vulnerability reporting
```

## Directory Descriptions

### `.github/`

Contains all GitHub-specific configuration files:

- **`ISSUE_TEMPLATE/`**: Templates for creating structured issues
  - `bug_report.md`: Helps users report bugs with all necessary information
  - `feature_request.md`: Guides users in proposing new features

- **`workflows/`**: GitHub Actions workflow definitions
  - `docs.yml`: Documentation build and deployment to GitHub Pages
  - `full-build.yml`: Comprehensive build pipeline with linting, testing, and type checking
  - `security-scanning.yml`: Security scanning with Bandit that runs after successful builds

- **`PULL_REQUEST_TEMPLATE.md`**: Template that appears when creating pull requests

### Root Directory Files

#### Documentation Files

- **`README.md`**: The main entry point for the repository. Contains:
  - Project overview
  - Installation instructions
  - Usage guidelines
  - Links to other documentation

- **`CONTRIBUTING.md`**: Guidelines for contributors including:
  - How to report bugs
  - How to suggest features
  - Development workflow
  - Coding standards
  - Commit message guidelines

- **`CODE_OF_CONDUCT.md`**: Defines expected behavior for community members:
  - Standards of behavior
  - Enforcement policies
  - Reporting guidelines

- **`SECURITY.md`**: Security policy including:
  - How to report vulnerabilities
  - Supported versions
  - Security best practices

- **`FOLDER_STRUCTURE.md`**: This document explaining the repository organization

- **`LICENSE`**: MIT License for the project

#### Configuration Files

- **`.gitignore`**: Specifies files and directories that Git should ignore:
  - Operating system files
  - IDE configurations
  - Build artifacts
  - Dependencies
  - Temporary files
  - Environment variables

### Source Code Directories

#### `horizon_core/`
The main Python package containing secure logging utilities:

- **`__init__.py`**: Package initialization and public API exports
  - Exports `setup_logger` function for creating secure loggers
- **`logging.py`**: Secure logging utilities with automatic sensitive data redaction
  - `SecureLogger` class that extends standard Python logging
  - `SensitiveDataFormatter` that redacts sensitive information from log messages
  - `setup_logger()` function for easy logger configuration
  - Automatic detection and redaction of passwords, API keys, tokens, and other sensitive data
- **`cli_framework.py`**: Empty file (functionality removed in refactor)
- **`sarif.py`**: Empty file (functionality removed in refactor)
- **`config.py`**: Empty file (functionality removed in refactor)

#### `tests/`
Contains all test files for the project:
- `test_logging.py`: Comprehensive tests for secure logging functionality including:
  - Tests for `SecureLogger` class methods
  - Tests for `SensitiveDataFormatter` redaction patterns
  - Tests for `setup_logger` function
  - Edge cases and error handling tests
- `test_cli_framework.py`: Empty file (tests removed in refactor)
- `test_sarif.py`: Empty file (tests removed in refactor)  
- `test_config.py`: Empty file (tests removed in refactor)

Tests use pytest and aim for comprehensive coverage of the logging module.

#### `docs/`
Contains additional documentation beyond the root-level markdown files:
- API documentation
- User guides
- Architecture documentation
- Development guides

See `docs/README.md` for the documentation index.

#### `config/`
Contains configuration files for different environments and tools:
- Development environment configuration
- Staging environment configuration
- Production environment configuration
- Tool-specific configurations

See `config/README.md` for configuration documentation.

## File Naming Conventions

- **Markdown files**: Use `UPPERCASE.md` for root-level documentation (e.g., `README.md`, `CONTRIBUTING.md`)
- **Template files**: Use `lowercase_with_underscores.md` (e.g., `bug_report.md`, `feature_request.md`)
- **Configuration files**: Follow the convention of the tool (e.g., `.gitignore`, `ci.yml`)
- **Source code**: Follow language-specific conventions (e.g., camelCase, snake_case)

## Best Practices

1. **Keep root directory clean**: Only essential files should be in the root
2. **Organize by feature**: Group related files together
3. **Use meaningful names**: File and directory names should be self-explanatory
4. **Document structure**: Update this file when adding new directories
5. **Ignore generated files**: Add build artifacts and dependencies to `.gitignore`
6. **Follow conventions**: Maintain consistency with established patterns

## Adding New Directories

When adding new directories to the project:

1. Create the directory with a clear, descriptive name
2. Add a `README.md` in the directory explaining its purpose
3. Update this `FOLDER_STRUCTURE.md` file with the new directory
4. Update `.gitignore` if the directory contains generated files
5. Document any special conventions for files in that directory

## Questions?

If you have questions about where a file should go or how to organize your code, refer to:
- This document
- The `CONTRIBUTING.md` file for contribution guidelines
- Open an issue to discuss structural changes
