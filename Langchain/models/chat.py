from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.schema import SystemMessage, HumanMessage, AIMessage
from dotenv import load_dotenv

load_dotenv()
model = ChatGoogleGenerativeAI(model="gemini-2.5-flash", temperature=0)

chatHistory = [
    SystemMessage(content="You are a helpful assistant.")
]

while True:
    userInput = input("User: ")
    if userInput == "bye":
        break

    chatHistory.append(HumanMessage(content=userInput))
    result = model.invoke(chatHistory)
    chatHistory.append(AIMessage(content=result.content))
    print("AI:", result.content)
