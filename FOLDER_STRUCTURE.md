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
│   │   └── ci.yml                  # Continuous integration workflow
│   └── PULL_REQUEST_TEMPLATE.md    # Template for pull requests
├── config/                          # Configuration files
│   └── README.md                   # Configuration documentation
├── docs/                            # Additional documentation
│   └── README.md                   # Documentation index
├── src/                             # Source code directory
│   └── README.md                   # Source code documentation
├── tests/                           # Test files
│   └── README.md                   # Testing documentation
├── CODE_OF_CONDUCT.md               # Community code of conduct
├── CONTRIBUTING.md                  # Contribution guidelines
├── FOLDER_STRUCTURE.md              # This file - describes repository structure
├── LICENSE                          # MIT License
├── README.md                        # Main project documentation
├── SECURITY.md                      # Security policy and vulnerability reporting
└── .gitignore                       # Git ignore patterns
```

## Directory Descriptions

### `.github/`

Contains all GitHub-specific configuration files:

- **`ISSUE_TEMPLATE/`**: Templates for creating structured issues
  - `bug_report.md`: Helps users report bugs with all necessary information
  - `feature_request.md`: Guides users in proposing new features

- **`workflows/`**: GitHub Actions workflow definitions
  - `ci.yml`: Continuous integration workflow that runs tests and checks

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

#### `src/`
Contains the source code for Horizon Core. This directory will include:
- Core components and modules
- Utility functions and helpers
- Service implementations
- Business logic

See `src/README.md` for detailed information about the source code organization.

#### `tests/`
Contains all test files for the project:
- Unit tests
- Integration tests
- End-to-end tests
- Test utilities and fixtures

See `tests/README.md` for detailed information about testing.

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
