from langchain_core.messages import HumanMessage
from graph import app

if __name__ == "__main__":
    print("AI Buddy (LangGraph MCP). Type 'exit' to quit.\n")

    state = {
        "messages": [],
    }

    while True:
        user_input = input("You: ")
        if user_input.lower() == "exit":
            break

        state["messages"].append(HumanMessage(content=user_input))

        state = app.invoke(state)

        last_message = state["messages"][-1]
        print("\nBuddy:", last_message.content, "\n")
