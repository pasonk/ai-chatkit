from langgraph_supervisor import create_supervisor
from langgraph.prebuilt import create_react_agent
from ai.llm import get_model, settings
from langgraph.checkpoint.memory import InMemorySaver
from langgraph_supervisor.handoff import create_forward_message_tool


from dotenv import load_dotenv  # 用于加载环境变量
load_dotenv()  # 加载 .env 文件中的环境变量

from langchain.globals import set_debug
from langchain.globals import set_verbose

set_debug(True)
set_verbose(False)

model = get_model(settings.DEFAULT_MODEL)

math_agent = create_react_agent(
    model=model,
    prompt="You are a math expert, calculating step by step and answering users' math questions, don't answer questions related to programming",
    tools=[],
    name="math_agent"
).with_config(tags=["skip_stream"])

# 编程专家智能体
code_agent = create_react_agent(
    model=model,
    prompt="You are a programming expert. Solve users' programming problems, don't answer questions related to math",
    tools=[],
    name="code_agent"
).with_config(tags=["skip_stream"])

# 通用智能体
general_agent = create_react_agent(
    model=model,
    prompt="You are a universal assistant. Answer all questions from users except those related to math and programming",
    tools=[],
    name="general_agent"
).with_config(tags=["skip_stream"])

forwarding_tool = create_forward_message_tool("supervisor") # The argument is the name to assign to the resulting forwarded message

# 创建一个监督者
supervisor = create_supervisor(
    agents=[general_agent, code_agent, math_agent],
    model=model,
    # full_history 全消息记录，last_message 最后智能体的输出
    output_mode="last_message",
    prompt=(
       """
       You are a supervisor managing the following agents:
        - math_agent: Handles math, calculations, algebra, etc.
        - code_agent: Handles programming, algorithms, code-related questions.
        - general_agent: Handles other general questions.
        
        Based on the user's question, please select the most appropriate agent to handle the question.
        if the question is about math or programming, please select the math_agent or code_agent, if the question is about other general questions, please select the general_agent.
        If there are programming issues and math_agent outputs results related to programming, code_agent still needs to be used to re-obtain the result of the programming problem, and the programming result shall be based on the output of code_agent.
        Finally, the supervisor summarizes the output results.
        Note: Only one tool can be called at a time; multiple tools cannot be called parallel.

        """
    ),
    
    add_handoff_back_messages=False,
    parallel_tool_calls=False,
    tools=[forwarding_tool]

)

checkpointer = InMemorySaver()

supervisor_agent = supervisor.compile(checkpointer=checkpointer)

