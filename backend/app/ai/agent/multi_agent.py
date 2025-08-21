from langgraph_supervisor import create_supervisor
from langgraph.prebuilt import create_react_agent
from ai.llm import get_model, settings
from langgraph.checkpoint.memory import InMemorySaver
from langgraph_supervisor.handoff import create_forward_message_tool


from dotenv import load_dotenv
load_dotenv()

from langchain.globals import set_debug
from langchain.globals import set_verbose

set_debug(True)
set_verbose(False)

model = get_model(settings.DEFAULT_MODEL)
#  Agent
math_agent = create_react_agent(
    model=model,
    prompt="You are a math expert, calculating step by step and answering users' math questions, don't answer questions related to programming",
    tools=[],
    name="math_agent"
).with_config(tags=["skip_stream"])

# Programming expert agent
code_agent = create_react_agent(
    model=model,
    prompt="You are a programming expert. Solve users' programming problems, don't answer questions related to math",
    tools=[],
    name="code_agent"
).with_config(tags=["skip_stream"])

# General agent
general_agent = create_react_agent(
    model=model,
    prompt="You are a universal assistant. Answer all questions from users except those related to math and programming",
    tools=[],
    name="general_agent"
).with_config(tags=["skip_stream"])

forwarding_tool = create_forward_message_tool("supervisor") # The argument is the name to assign to the resulting forwarded message

# Create a supervisor
supervisor = create_supervisor(
    agents=[general_agent, code_agent, math_agent],
    model=model,
    # full_history full message record, last_message output of the last agent
    output_mode="last_message",
    prompt=(
       """
       You are a supervisor managing the following agents:
        - math_agent: Handles math, calculations, algebra, etc.
        - code_agent: Handles programming, algorithms, code-related questions.
        - general_agent: Handles other general questions.
        
        Based on the user's question, please select the most appropriate agent to handle the question.
        if the question is about math or programming, please select the math_agent or code_agent, if the question is about other general questions, please select the general_agent.
        If the agent you manage has already provided the answer, you can directly return the answer without having to think again yourself.

        Note: Only one tool can be called at a time; multiple tools cannot be called parallel.

        """
    ),
    
    add_handoff_back_messages=False,
    parallel_tool_calls=False,
    tools=[forwarding_tool]

)

checkpointer = InMemorySaver()

supervisor_agent = supervisor.compile(checkpointer=checkpointer)

