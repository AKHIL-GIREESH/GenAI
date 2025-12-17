from langchain_ollama import ChatOllama
from langchain_core.messages import SystemMessage, HumanMessage, AIMessage
from dotenv import load_dotenv

load_dotenv()
model = ChatOllama(model="mistral:7b", temperature=0)

chatHistory = [
    SystemMessage(content="You are this very extroverted and outgoing human friend (ESTP).")
]

while True:
    userInput = input("User: ")
    if userInput == "bye":
        break

    chatHistory.append(HumanMessage(content=userInput))
    result = model.invoke(chatHistory)
    chatHistory.append(AIMessage(content=result.content))
    print("AI:", result.content)
