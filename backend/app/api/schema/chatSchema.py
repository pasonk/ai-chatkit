from pydantic import BaseModel, Field, SerializeAsAny
from typing import Any, Literal, NotRequired
from typing_extensions import TypedDict
from ai.agent.agents import DEFAULT_AGENT


class UserInput(BaseModel):
    """user chat input info"""

    message: str = Field(
        description="input message"
    )

    thread_id: str | None = Field(
        description="Thread ID is used for persistence and continuing multi-round conversations",
        default=None
    )
    
    agent_id: str | None = Field(
        description="a agent id",
        default=DEFAULT_AGENT
    )
    
    agent_config: dict[str, Any] = Field(
        description="Additional configuration to pass through to the agent",
        default={},
        examples=[{"spicy_level": 0.8}],
    )
    
class ToolCall(TypedDict):
    """Represents a request to call a tool."""

    name: str
    """The name of the tool to be called."""
    args: dict[str, Any]
    """The arguments to the tool call."""
    id: str | None
    """An identifier associated with the tool call."""
    type: NotRequired[Literal["tool_call"]]

class ChatMessage(BaseModel):
    """ A message in a chat."""

    type: Literal["human", "ai", "tool", "custom"] = Field(
        description="Role of the message.",
        examples=["human", "ai", "tool", "custom"],
    )
    content: str = Field(
        description="Content of the message.",
        examples=["Hello, world!"],
    )
    tool_calls: list[ToolCall] = Field(
        description="Tool calls in the message.",
        default=[],
    )
    tool_call_id: str | None = Field(
        description="Tool call that this message is responding to.",
        default=None,
    )
    run_id: str | None = Field(
        description="Run ID of the message.",
        default=None,
    )
    response_metadata: dict[str, Any] = Field(
        description="Response metadata. For example: response headers, logprobs, token counts.",
        default={},
    )
    custom_data: dict[str, Any] = Field(
        description="Custom message data.",
        default={},
    )
    
class StreamInput(UserInput):
    """User input for streaming the agent's response."""

    stream_tokens: bool = Field(
        description="Whether to stream LLM tokens to the client.",
        default=True,
    )
