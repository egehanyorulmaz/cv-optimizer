# Core Directory

Contains the essential business logic and domain models of the application. This directory should be kept clean of external dependencies.

## Structure

- `domain/` - Core business entities and value objects
- `ports/` - Interface definitions for external dependencies
- `services/` - Core business services and use cases

## Guidelines

1. No external dependencies allowed (except standard library)
2. All external interactions must go through port interfaces
3. Domain models should be immutable when possible
4. Use type hints and dataclasses for domain models
5. Keep business rules and validation logic here

## Testing

- All core logic should have comprehensive unit tests
- Tests should not require external dependencies
- Use mocks for testing port interfaces 