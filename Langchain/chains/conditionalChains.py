from tempfile import template
from dotenv import load_dotenv
from langchain_core.output_parsers import StrOutputParser,PydanticOutputParser
from langchain_core.prompts import PromptTemplate
from langchain_core.runnables import RunnableBranch,RunnableLambda
from langchain_google_genai import ChatGoogleGenerativeAI
from pydantic import BaseModel, Field
from typing import Literal

load_dotenv()

model = ChatGoogleGenerativeAI(model="gemini-2.5-flash")
parser = StrOutputParser()

class Feedback(BaseModel):
    sentiment: Literal['positive','negative'] = Field(description="Give the sentiment of the feedback")

parser2 = PydanticOutputParser(pydantic_object=Feedback)

prompt1 = PromptTemplate(
    template = "Classify the give sentiment into positive or negative: \n{feedback}\n{format_instruction}",
    input_variables=["topic"],
    partial_variables={'format_instruction':parser2.get_format_instructions()}
)

prompt2 = PromptTemplate(
    template = "Write an appropraite response to this positive feedback \n {feedback}",
    input_variables=["feedback"]
)

prompt3 = PromptTemplate(
    template = "Write an appropraite response to this negative feedback \n {feedback}",
    input_variables=["feedback"]
)

classiferChain = prompt1 | model | parser2

brachChain = RunnableBranch(
    (lambda x:x.sentiment == 'positive', prompt2 | model | parser),
    (lambda x:x.sentiment == 'negative', prompt3 | model | parser),
    RunnableLambda(lambda x: "Could not find Sentiment")
)

chain = classiferChain | brachChain

result = chain.invoke({'feedback':'This is a trash product'})
print(result)
