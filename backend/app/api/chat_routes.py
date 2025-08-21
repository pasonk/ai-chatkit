import logging
from core.config import settings
from fastapi import APIRouter, status
from fastapi.exceptions import HTTPException
from fastapi.responses import StreamingResponse

from uuid import UUID, uuid4
from langchain_core.messages import AIMessage, AIMessageChunk, AnyMessage, HumanMessage, ToolMessage
from langchain_core.runnables import RunnableConfig
from langgraph.types import Command, Interrupt
from api.schema.chatSchema import UserInput, ChatMessage, StreamInput
from asyncio import CancelledError
from ai.agent.agents import get_agent, DEFAULT_AGENT, CompiledStateGraph
from typing import Any, Union, Dict, List, Optional
from utils.chat_utils import langchain_to_chat_message, remove_tool_calls, convert_message_content_to_string
from collections.abc import AsyncGenerator
import json

logger = logging.getLogger(__name__)


chat_router = APIRouter(prefix="/chat", tags=["chat"],)

@chat_router.post("/invoke")
async def invoke(user_input: UserInput) -> ChatMessage:
    """
    Use user input to invoke a proxy to get the final response.

    If no agent_id is provided, the default proxy will be used.
    Use thread_id to persist and continue multi-turn dialogues. The run_id keyword argument will also be attached to the message for recording feedback.
    """
    agent: CompiledStateGraph = get_agent(user_input.agent_id)
    
    kwargs, run_id = await _handle_input(user_input, agent)
    try:
        response_events = await agent.ainvoke(**kwargs, stream_mode=["updates", "values"])
        response_type, response = response_events[-1]
        if response_type == "values":
            # Normal response, the agent completed successfully
            output = langchain_to_chat_message(response["messages"][-1])
        elif response_type == "updates" and "__interrupt__" in response:
            # The last thing to occur was an interrupt
            # Return the value of the first interrupt as an AIMessage
            output = langchain_to_chat_message(
                AIMessage(content=response["__interrupt__"][0].value)
            )
        else:
            raise ValueError(f"Unexpected response type: {response_type}")

        output.run_id = str(run_id)
        return output
    except Exception as e:
        logger.error(f"An exception occurred: {e}")
        raise HTTPException(status_code=500, detail="Unexpected error")
    
    
@chat_router.post("/stream", response_class=StreamingResponse, responses=_sse_response_example())
async def stream(user_input: StreamInput) -> StreamingResponse:
    """
    流式传输代理的响应。
    
    """

    return StreamingResponse(
        message_generator(user_input),
        media_type="text/event-stream",
    )


async def _handle_input(
    user_input: UserInput, agent: CompiledStateGraph
) -> tuple[dict[str, Any], UUID]:
    """
    Parse user input and handle any required interrupt resumption.
    Returns kwargs for agent invocation and the run_id.
    """
    run_id = uuid4()
    thread_id = user_input.thread_id or str(uuid4())

    configurable = {"thread_id": thread_id, "model": settings.DEFAULT_MODEL}

    # Check whether agent_config exists in user_input
    if user_input.agent_config:
        # Find the intersection of the keys in the configurable dictionary and the keys in the user_input.agent_config dictionary
        overlap = configurable.keys() & user_input.agent_config.keys()
        if overlap:
            # If there is an intersection, it means that agent_config contains reserved keys, throw an HTTP exception
            raise HTTPException(
                status_code=422,
                detail=f"agent_config contains reserved keys: {overlap}",
            )
    # If there is no intersection, update the content of user_input.agent_config to the configurable dictionary
    configurable.update(user_input.agent_config)

    config = RunnableConfig(
        configurable=configurable,
        run_id=run_id,
    )

    # Check for interrupts that need to be resumed
    state = await agent.aget_state(config=config)
    interrupted_tasks = [
        task for task in state.tasks if hasattr(task, "interrupts") and task.interrupts
    ]

    if interrupted_tasks:
        # assume user input is response to resume agent execution from interrupt
        input = Command(resume=user_input.message)
    else:
        input = {"messages": [HumanMessage(content=user_input.message)]}

    kwargs = {
        "input": input,
        "config": config,
    }

    return kwargs, run_id

def _sse_response_example() -> dict[int, Any]:
    return {
        status.HTTP_200_OK: {
            "description": "Server Sent Event Response",
            "content": {
                "text/event-stream": {
                    "example": "data: {'type': 'token', 'content': 'Hello'}\n\ndata: {'type': 'token', 'content': ' World'}\n\ndata: end\n\n",
                    "schema": {"type": "string"},
                }
            },
        }
    }


async def message_generator(
    user_input: StreamInput
) -> AsyncGenerator[str, None]:
    """
    An asynchronous generator for generating messages, used for the responses of streaming agents.
    """
    agent: CompiledStateGraph = get_agent(user_input.agent_id)
    kwargs, run_id = await _handle_input(user_input, agent)

    try:
        async for stream_event in agent.astream(
            **kwargs, stream_mode=["updates", "messages", "custom"]
        ):
            if not isinstance(stream_event, tuple):
                continue
            stream_mode, event = stream_event
            new_messages = []
            if stream_mode == "updates":
                for node, updates in event.items():
                    # A simple approach to handle agent interrupts.
                    if node == "__interrupt__":
                        interrupt: Interrupt
                        for interrupt in updates:
                            new_messages.append(AIMessage(content=interrupt.value))
                        continue
                    update_messages = updates.get("messages", [])
 
                     # Only retain the output of "supervisor"
                    if node == "supervisor":
                        if isinstance(update_messages[-1], AIMessage):
                            update_messages = [update_messages[-1]]
                        elif isinstance(update_messages[-1], ToolMessage):
                            if len(update_messages) > 1:
                                update_messages = [update_messages[-2],update_messages[-1]]
                            else:
                                update_messages = [update_messages[-1]]
                        else:
                            update_messages = []
                    if node in ("math_agent", "code_agent"):
                        update_messages = []
                    new_messages.extend(update_messages)

            if stream_mode == "custom":
                new_messages = [event]

            for message in new_messages:
                try:
                    chat_message = langchain_to_chat_message(message)
                    chat_message.run_id = str(run_id)
                except Exception as e:
                    logger.error(f"Error parsing message: {e}")
                    yield f"data: {json.dumps({'type': 'error', 'content': 'Unexpected error'})}\n\n"
                    continue
                if chat_message.type == "human" and chat_message.content == user_input.message:
                    continue
                yield f"data: {json.dumps({'type': 'message', 'content': chat_message.model_dump()})}\n\n"

            if stream_mode == "messages":
                if not user_input.stream_tokens:
                    continue
                msg, metadata = event
                if "skip_stream" in metadata.get("tags", []):
                    continue

                if not isinstance(msg, AIMessageChunk):
                    continue
                content = remove_tool_calls(msg.content)
                if content:
                    yield f"data: {json.dumps({'type': 'token', 'content': convert_message_content_to_string(content)})}\n\n"
    except GeneratorExit:
        # Handle GeneratorExit gracefully
        logger.info("Stream closed by client")
        return
    except CancelledError:
        # Handle CancelledError gracefully
        logger.info("Stream cancelled")
        return
    except Exception as e:
        logger.error(f"Error in message generator: {e}")
        yield f"data: {json.dumps({'type': 'error', 'content': str(e)})}\n\n"
    finally:
        yield f"data: {json.dumps({'type': 'end'})}\n\n"


