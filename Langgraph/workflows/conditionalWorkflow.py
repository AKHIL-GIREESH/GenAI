from typing import TypedDict
from langgraph.graph import START,StateGraph, END

class CalcState(TypedDict):
    a: int
    b: int
    op: str
    result: int

def add(state: CalcState):
    return {"result": state["a"] + state["b"]}

def subtract(state: CalcState):
    return {"result": state["a"] - state["b"]}

def route(state: CalcState):
    if state["op"] == "+":
        return "add"
    else:
        return "subtract"

graph = StateGraph(CalcState)

graph.add_node("add", add)
graph.add_node("subtract", subtract)

graph.add_edge(START, "route")
graph.add_conditional_edges(
    source="route",
    path=route,
    path_map={
        "add": "add",
        "subtract": "subtract"
    }
)

graph.set_entry_point("route")

graph.add_edge("add", END)
graph.add_edge("subtract", END)

app = graph.compile()

result = app.invoke({
    "a": 10,
    "b": 5,
    "op": "+"
})

print(result)
