# Tests

This directory contains all test files for Horizon Core.

## Structure

As the project develops, tests will be organized into:

- **unit/**: Unit tests for individual components and functions
- **integration/**: Integration tests for multiple components working together
- **e2e/**: End-to-end tests for complete workflows
- **fixtures/**: Test data and fixtures
- **helpers/**: Test utilities and helper functions

## Testing Guidelines

When writing tests:

1. **Write comprehensive tests**: Aim for high code coverage
2. **Test edge cases**: Include tests for boundary conditions and error cases
3. **Keep tests isolated**: Each test should be independent and not rely on others
4. **Use descriptive names**: Test names should clearly describe what is being tested
5. **Follow existing patterns**: Maintain consistency with existing test structure

## Running Tests

Instructions for running tests will be added as the testing framework is established:

```bash
# Run all tests
# Command will be added

# Run specific test suite
# Command will be added

# Run with coverage
# Command will be added
```

## Test Organization

- Group related tests together
- Mirror the structure of the `src/` directory when possible
- Keep test files close to the code they test (or follow the established pattern)

## Questions?

If you have questions about testing:
- Check the [CONTRIBUTING.md](../CONTRIBUTING.md) for testing guidelines
- Review existing tests for examples
- Open an issue for discussion
