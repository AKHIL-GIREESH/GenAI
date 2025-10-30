from dotenv import load_dotenv
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import PromptTemplate
from langchain_core.runnables import RunnableParallel
from langchain_google_genai import ChatGoogleGenerativeAI

load_dotenv()

prompt1 = PromptTemplate(
    template = "Generate a detailed report on {topic}",
    input_variables=["topic"]
)

prompt2 = PromptTemplate(
    template = "Condense it down into 5 points {text}",
    input_variables=["text"]
)

prompt3 = PromptTemplate(
    template = "Condense it down into 5 questions {text}",
    input_variables=["text"] 
)

prompt4 = PromptTemplate(
    template = "Merge the two into a single document:\Summary {notes} \nQuestions {questions}",
    input_variables=["text"] 
)

model = ChatGoogleGenerativeAI(model="gemini-2.5-flash")
parser = StrOutputParser()

parallelChain = RunnableParallel({
    'notes': prompt2 | model | parser,
    'questions': prompt3 | model | parser
})

chain = prompt1 | model | parser | parallelChain | prompt4 | model | parser

result = chain.invoke({'topic':'AI Companions'})
print(result)
