from cv_optimizer.core.domain.agents import (
    Agent,
    AgentResponse,
    AgentType,
    OptimizationContext,
)
from cv_optimizer.core.ports.ai_provider import AIProvider, AIOptions
from typing import List


class CriticAgent(Agent):
    def __init__(self, ai_provider: AIProvider):
        self.ai_provider = ai_provider

    async def process(self, context: OptimizationContext) -> AgentResponse:
        prompt = self._build_critique_prompt(context.resume)

        critique = await self.ai_provider.complete(
            prompt=prompt, options=AIOptions(temperature=0.7)
        )

        # Parse the critique into structured suggestions
        suggestions = self._parse_critique(critique)

        return AgentResponse(
            agent_type=AgentType.CRITIC,
            suggestions=suggestions,
            confidence_score=0.8,
            metadata={"raw_critique": critique},
        )

    def _build_critique_prompt(self, resume) -> str:
        # Implementation of prompt building
        pass

    def _parse_critique(self, critique: str) -> List[str]:
        # Implementation of critique parsing
        pass
