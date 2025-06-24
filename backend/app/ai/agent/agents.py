from dataclasses import dataclass

from langgraph.graph.state import CompiledStateGraph
from pydantic import BaseModel, Field
from ai.agent.oa_assistant import oa_assistant

DEFAULT_AGENT = "oa-assistant"

class AgentInfo(BaseModel):
    """Info about an available agent."""

    key: str = Field(
        description="Agent key.",
        examples=["oa-assistant"],
    )
    description: str = Field(
        description="Description of the agent.",
        examples=["A oa assistant for company"],
    )

@dataclass
class Agent:
    description: str
    graph: CompiledStateGraph


agents: dict[str, Agent] = {
    "oa-assistant": Agent(description="A oa intelligent assistant.", graph=oa_assistant),
}


def get_agent(agent_id: str) -> CompiledStateGraph:
    return agents[agent_id].graph


def get_all_agent_info() -> list[AgentInfo]:
    return [
        AgentInfo(key=agent_id, description=agent.description) for agent_id, agent in agents.items()
    ]
