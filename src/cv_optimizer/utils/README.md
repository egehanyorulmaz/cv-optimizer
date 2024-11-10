# Utils Directory

Contains shared utilities and helper functions used across the application.

## Structure

- `logging.py` - Logging configuration and utilities
- `config.py` - Configuration management
- `exceptions.py` - Custom exception definitions
- `validators.py` - Shared validation utilities

## Guidelines

1. Keep utilities focused and single-purpose
2. Avoid business logic in utilities
3. Make utilities stateless when possible
4. Document all public functions and classes
5. Include comprehensive error handling

## Adding New Utilities

1. Create focused utility modules
2. Add comprehensive unit tests
3. Document usage and examples
4. Avoid circular dependencies
5. Keep external dependencies minimal 