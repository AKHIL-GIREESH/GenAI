from langchain_google_genai import ChatGoogleGenerativeAI
from dotenv import load_dotenv
from langchain_core.prompts import PromptTemplate,load_prompt


load_dotenv()
model = ChatGoogleGenerativeAI(model="gemini-2.5-flash", temperature=0)
template = load_prompt("philosopher_prompt.json")
prompt = template.invoke({"text":"Gucci is expensive no cap"})
result = model.invoke(prompt)
print(result.content)
