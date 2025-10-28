# Contributing to Horizon Core

First off, thank you for considering contributing to Horizon Core! It's people like you that make this secure logging library better for everyone in the HorizonSec organization.

## Table of Contents

- [Code of Conduct](#code-of-conduct)
- [How Can I Contribute?](#how-can-i-contribute)
  - [Reporting Bugs](#reporting-bugs)
  - [Suggesting Features](#suggesting-features)
  - [Submitting Pull Requests](#submitting-pull-requests)
- [Development Workflow](#development-workflow)
- [Coding Standards](#coding-standards)
- [Commit Message Guidelines](#commit-message-guidelines)

## Code of Conduct

This project and everyone participating in it is governed by our [Code of Conduct](CODE_OF_CONDUCT.md). By participating, you are expected to uphold this code. Please report unacceptable behavior to the project maintainers.

## How Can I Contribute?

### Reporting Bugs

Bugs are tracked as GitHub issues. When creating a bug report, please use the bug report template and include:

- **Clear and descriptive title** for the issue
- **Detailed description** of the problem
- **Steps to reproduce** the behavior
- **Expected behavior** vs actual behavior
- **Screenshots** if applicable
- **Environment details** (OS, browser, versions, etc.)
- **Additional context** that might be helpful

**Before submitting a bug report:**
- Check the existing issues to avoid duplicates
- Verify the bug in the latest version
- Collect relevant information about your environment

### Suggesting Features

Feature requests are also tracked as GitHub issues. When creating a feature request, please use the feature request template and include:

- **Clear and descriptive title** for the suggestion
- **Detailed description** of the proposed feature
- **Use cases** explaining why this feature would be useful
- **Alternatives** you've considered
- **Additional context** like mockups or examples

**Before submitting a feature request:**
- Check if the feature already exists
- Review existing feature requests
- Consider if the feature aligns with the project's goals

### Submitting Pull Requests

We actively welcome your pull requests! Here's how to contribute code:

1. **Fork the repository** and create your branch from `main`
2. **Make your changes** following our coding standards
3. **Test your changes** thoroughly
4. **Update documentation** as needed
5. **Write clear commit messages** following our guidelines
6. **Submit a pull request** using the PR template

**Pull Request Process:**
- Fill out the PR template completely
- Link related issues using keywords (e.g., "Fixes #123")
- Ensure all tests pass
- Request review from maintainers
- Address review feedback promptly
- Keep your PR focused on a single concern

**Pull Request Requirements:**
- [ ] Code follows the project's coding standards
- [ ] Self-review of code completed
- [ ] Comments added for complex code
- [ ] Documentation updated
- [ ] No new warnings generated
- [ ] Tests added/updated and passing
- [ ] Dependent changes merged and published

## Development Workflow

### Setting Up Development Environment

1. Clone your fork:
   ```bash
   git clone https://github.com/your-username/horizon-core.git
   cd horizon-core
   ```

2. Add upstream remote:
   ```bash
   git remote add upstream https://github.com/HorizonSec/horizon-core.git
   ```

3. Install Hatch (if not already installed):
   ```bash
   pip install hatch
   ```

4. Set up development environment:
   ```bash
   hatch env create dev
   ```

3. Create a feature branch:
   ```bash
   git checkout -b feature/your-feature-name
   ```

### Making Changes

1. Make your changes in your feature branch
2. Format your code:
   ```bash
   hatch run format
   ```
3. Run type checking:
   ```bash
   hatch run dev:typecheck
   ```
4. Run linting checks:
   ```bash
   hatch run pre-build
   ```
5. Test your changes:
   ```bash
   hatch run test
   hatch run test-cov
   ```
6. Run security checks:
   ```bash
   hatch run dev:bandit -r ./horizon_core
   ```
7. Commit your changes with clear messages
8. Push to your fork

### Syncing with Upstream

Keep your fork synchronized with the upstream repository:

```bash
git fetch upstream
git checkout main
git merge upstream/main
```

## Coding Standards

### General Guidelines

- **Write clear, readable code** - Code is read more often than written
- **Keep it simple** - Avoid unnecessary complexity
- **Follow existing patterns** - Maintain consistency with the codebase
- **Comment wisely** - Explain why, not what
- **Test your code** - Write comprehensive tests for new functionality
- **Security first** - Be mindful of sensitive data handling in logging code
- **Python 3.9+** - Ensure compatibility with Python 3.9 and higher

### Style Guide

- **Black formatting**: Code is automatically formatted with Black (line length: 100)
- **Import organization**: Use isort for consistent import ordering
- **Type hints**: Add type hints for all function parameters and return values
- **Docstrings**: Use Google-style docstrings for all public functions and classes
- **Variable names**: Use descriptive names that clearly indicate purpose
- **Line length**: Maximum 100 characters (enforced by Black)
- **Flake8 compliance**: Code must pass flake8 linting checks

### Documentation

- Update README.md for user-facing changes
- Update inline documentation for code changes
- Add comments for complex logic
- Keep documentation concise and clear

## Commit Message Guidelines

Write clear, concise commit messages that explain the changes:

### Format

```
<type>: <subject>

<body>

<footer>
```

### Type

- **feat**: New feature
- **fix**: Bug fix
- **docs**: Documentation changes
- **style**: Code style changes (formatting, etc.)
- **refactor**: Code refactoring
- **test**: Adding or updating tests
- **chore**: Maintenance tasks

### Examples

```
feat: add bug report template

Added a comprehensive bug report template to improve issue quality
and make it easier for contributors to report issues effectively.

Closes #123
```

```
fix: correct typo in README

Fixed spelling error in installation instructions.
```

### Best Practices

- Use imperative mood ("add feature" not "added feature")
- Keep subject line under 50 characters
- Capitalize the subject line
- Don't end subject line with a period
- Separate subject from body with a blank line
- Wrap body at 72 characters
- Use body to explain what and why, not how

## Questions?

If you have questions about contributing, feel free to:
- Open an issue with your question
- Reach out to the maintainers
- Check existing documentation

Thank you for contributing to Horizon Core! 🎉
