from langchain_ollama import ChatOllama

llm = ChatOllama(
    model="mistral:7b",
    temperature=0
)
