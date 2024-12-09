# Source Code Directory

This directory contains the main application code organized following hexagonal architecture principles. For more details about the design principles, please refer to [system design principles](https://www.geeksforgeeks.org/hexagonal-architecture-system-design/).

## Structure

- `core/` - Core business logic and domain models
- `infrastructure/` - External implementations and adapters

## Guidelines

1. Keep the core domain logic independent of external implementations
2. All external dependencies should be abstracted through interfaces in `core/ports`
3. Follow dependency injection principles
4. Maintain clear separation of concerns between layers 
