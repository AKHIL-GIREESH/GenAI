from langgraph.graph import StateGraph
from langgraph.prebuilt import ToolNode
from langchain_core.messages import SystemMessage
from state import AgentState
from llm import llm
from tools.tool_registry import TOOLS
from prompts.system import SYSTEM_PROMPT

llm_with_tools = llm.bind_tools(TOOLS)
tool_node = ToolNode(TOOLS)

def agent_node(state: AgentState):
    messages = [SystemMessage(content=SYSTEM_PROMPT)] + state["messages"]
    response = llm_with_tools.invoke(messages)
    return {"messages": [response]}

def should_continue(state: AgentState):
    last_message = state["messages"][-1]
    if last_message.tool_calls:
        return "tools"
    return "__end__"

graph = StateGraph(AgentState)

graph.add_node("agent", agent_node)
graph.add_node("tools", tool_node)

graph.set_entry_point("agent")

graph.add_conditional_edges(
    "agent",
    should_continue,
    {
        "tools": "tools",
        "__end__": "__end__",
    },
)

graph.add_edge("tools", "agent")

app = graph.compile()
