from datetime import datetime
from typing import cast, Literal

from langchain.prompts import SystemMessagePromptTemplate
from langchain_core.language_models.chat_models import BaseChatModel
from langchain_core.messages import AIMessage, HumanMessage, SystemMessage
from langchain_core.runnables import RunnableConfig, RunnableLambda, RunnableSerializable
from langgraph.checkpoint.memory import MemorySaver
from langgraph.graph import END, MessagesState, StateGraph
from langgraph.prebuilt import ToolNode, tools_condition
from pydantic import BaseModel, Field

from ai.llm import get_model, settings
from ai.tools.oa_tools import get_user_department, get_user_info, search_handbook


from langchain.globals import set_debug
from langchain.globals import set_verbose
set_debug(True)
set_verbose(False)

import logging
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(filename)s[line:%(lineno)d] - %(funcName)s() - %(message)s')


class AgentState(MessagesState):
    """State of the agent."""

tools = [get_user_info, get_user_department, search_handbook]

def wrap_model(model: BaseChatModel) -> RunnableSerializable[AgentState, AIMessage]:
    model = model.bind_tools(tools)
    preprocessor = RunnableLambda(
        lambda state: [SystemMessage(content=instructions)] + state["messages"],
        name="StateModifier",
    )
    return preprocessor | model

instructions = """
    You are an assistant of a company's OA system, and your task is to help users query the administrative and personnel information within the company.
    You need to use tools to query relevant information from the database and knowledge base based on the user's questions and return it to the user.
    It is not allowed to forge the relevant regulations of the company at will to avoid misleading users out of thin air.
    You need to answer the users' questions and ensure the accuracy and completeness of the answers.
    You need to pay attention to the users' questions and avoid answering questions that they don't care about.
    The current time is：{current_time}
"""


async def call_model(state: AgentState, config: RunnableConfig) -> AgentState:
    """This node is to call llm model"""

    m = get_model(config["configurable"].get("model", settings.DEFAULT_MODEL))
    model_runnable = wrap_model(m)
    response = await model_runnable.ainvoke(state, config)

    return {"messages": [response]}



# After "model", if there are tool calls, run "tools". Otherwise END.
def pending_tool_calls(state: AgentState) -> Literal["tools", "done"]:
    last_message = state["messages"][-1]
    if not isinstance(last_message, AIMessage):
        raise TypeError(f"Expected AIMessage, got {type(last_message)}")
    if last_message.tool_calls:
        return "tools"
    return "done"


# Define the graph
agent = StateGraph(AgentState)
agent.add_node("model", call_model)
agent.add_node("tools", ToolNode(tools = tools))

agent.set_entry_point("model")
agent.add_edge("tools", "model")

agent.add_conditional_edges("model", pending_tool_calls, {"tools": "tools", "done": END})


oa_assistant = agent.compile(
    checkpointer=MemorySaver(),
)
oa_assistant.name = "oa_assistant"

# Save the graph as a PNG
# graph_png = oa_assistant.get_graph().draw_mermaid_png()

# with open("graph.png", "wb") as f:
#     f.write(graph_png)
