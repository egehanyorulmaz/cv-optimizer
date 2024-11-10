# Tests Directory

Contains all test files, mirroring the main source code structure.

## Structure

- `unit/` - Unit tests for individual components
- `integration/` - Integration tests for component interactions
- `e2e/` - End-to-end tests for complete workflows
- `fixtures/` - Test data and fixtures

## Guidelines

1. Mirror the src/ directory structure
2. Use pytest for testing
3. Keep tests independent and isolated
4. Use fixtures for shared test data
5. Maintain high test coverage

## Writing Tests

1. Follow AAA pattern (Arrange, Act, Assert)
2. Use meaningful test names
3. Include both positive and negative test cases
4. Mock external dependencies appropriately
5. Keep tests focused and single-purpose 