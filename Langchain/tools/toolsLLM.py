from langchain_core.tools import tool
from langchain_google_genai import ChatGoogleGenerativeAI
from dotenv import load_dotenv

@tool
def multiply(a:int,b:int) -> int:
    """ Multiply two numbers """
    print("Entered")
    return a*b

load_dotenv()
llm = ChatGoogleGenerativeAI(model="gemini-2.5-flash", temperature=0)

llm_with_tools = llm.bind_tools([multiply])
print(llm_with_tools.invoke('what is 10*7?').tool_calls)



