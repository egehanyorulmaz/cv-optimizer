# Infrastructure Directory

Contains implementations of external interfaces defined in `core/ports`. This is where we connect our application to the outside world.

## Structure

- `ai_providers/` - AI service implementations (OpenAI, Anthropic, etc.)
- `parsers/` - Document parser implementations
- `storage/` - Storage implementations
- `api/` - External API implementations

## Guidelines

1. Each implementation should implement a port interface from `core/ports`
2. Keep implementation details isolated from core business logic
3. Handle external errors and convert to domain exceptions
4. Use dependency injection for configuration
5. Implement proper error handling and logging

## Adding New Implementations

1. Create a new directory for the implementation category if needed
2. Implement the relevant port interface
3. Add necessary configuration handling
4. Include comprehensive error handling
5. Add integration tests 