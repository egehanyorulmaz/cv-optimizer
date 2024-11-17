# Architectural Guidelines

## Directory Structure

### 1. Core (`/core`)
- Contains the essential business logic and domain rules
- Should be framework and infrastructure-agnostic
- Contains:
  - Domain models and entities
  - Business rules and validation
  - Interface definitions (ports)
  - Pure business services that don't depend on external systems
  - Use cases/application services

Examples:
- Domain models (Resume, Experience, Education)
- Business rules validators
- Core interfaces/ports
- Pure business services (ResumeScorer, SkillMatcher)

### 2. Infrastructure (`/infrastructure`)
- Contains implementations of interfaces defined in core
- Handles external system interactions
- Contains:
  - Database implementations
  - External API clients
  - File system operations
  - Third-party service integrations
  - Framework-specific code

Examples:
- Database repositories
- AI provider implementations
- File parsers
- External API clients
- Email services

### 3. Application (`/application`)
- Contains use case implementations
- Orchestrates flow between domain and infrastructure
- Contains:
  - Use case implementations
  - Service orchestration
  - Transaction management
  - Event handling

Examples:
- Resume optimization orchestrator
- User registration flow
- Document processing pipeline

### 4. Interface (`/interface`)
- Contains entry points to the application
- Handles:
  - API controllers
  - CLI commands
  - Event handlers
  - GraphQL resolvers

### 5. Utils (`/utils`)
- Contains shared utilities
- Framework-agnostic helper functions
- Common tools and constants

## Decision Guidelines

1. Ask these questions when deciding where to place code:
   - Does it contain business rules? → Core
   - Does it interact with external systems? → Infrastructure
   - Is it an implementation detail? → Infrastructure
   - Is it orchestrating multiple services? → Application
   - Is it an entry point? → Interface
   - Is it a shared utility? → Utils

2. For specific cases:
   - If it's a service that could have multiple implementations → Define interface in Core, implement in Infrastructure
   - If it's purely business logic → Core
   - If it depends on external libraries → Infrastructure 