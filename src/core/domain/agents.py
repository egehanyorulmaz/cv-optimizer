from dataclasses import dataclass
from enum import Enum
from typing import Protocol, List, Any, Optional
from src.core.domain.resume import Resume


class AgentType(Enum):
    CRITIC = "critic"
    OPTIMIZER = "optimizer"
    LANGUAGE = "language"
    ATS = "ats"


@dataclass
class AgentResponse:
    agent_type: AgentType
    suggestions: List[str]
    confidence_score: float
    metadata: dict[str, Any]


@dataclass
class OptimizationContext:
    resume: Resume
    optimization_history: List[AgentResponse]
    target_job: Optional[str] = None
    industry: Optional[str] = None


class Agent(Protocol):
    async def process(self, context: OptimizationContext) -> AgentResponse:
        """Process the resume and return suggestions"""
        raise NotImplementedError("Agent.process is not implemented")
