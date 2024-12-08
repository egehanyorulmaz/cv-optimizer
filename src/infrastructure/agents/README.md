# Agents Directory

Contains implementations of different AI agents that process and optimize resumes.

## Structure

- `base.py` - Base agent interfaces and shared functionality
- `critic_agent.py` - Resume critique agent
- `optimizer_agent.py` - Resume optimization agent
- `language_agent.py` - Language improvement agent
- `ats_agent.py` - ATS optimization agent

## Guidelines

1. Each agent should have a single responsibility
2. Implement the Agent protocol from `core/domain/agents.py`
3. Keep prompt engineering logic separate from business logic
4. Use dependency injection for AI providers
5. Include proper error handling and logging

## Adding New Agents

1. Create a new file named `{purpose}_agent.py`
2. Implement the Agent protocol
3. Add unit tests in `tests/agents/`
4. Document the agent's purpose and behavior
5. Update the agent factory if using one 