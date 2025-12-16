from langgraph.graph import END, START, StateGraph
from langchain_google_genai import ChatGoogleGenerativeAI 
from typing import TypedDict
from dotenv import load_dotenv

load_dotenv()

model = ChatGoogleGenerativeAI(model="gemini-2.5-flash")

class LLMState(TypedDict):
    question: str
    answer: str

def llm_qna(state: LLMState) -> LLMState:
    question = f"What is the answer to {state['question']}?"
    answer = model.invoke(question)
    return {"question": question, "answer": answer}

graph = StateGraph(LLMState)
graph.add_node("llm_qna", llm_qna)
graph.add_edge(START, "llm_qna")
graph.add_edge("llm_qna", END)

workflow = graph.compile()

result = workflow.invoke({"question": "What is the capital of France?"})
print(result)
