from pydantic import BaseModel, Field
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
from typing import Optional, Literal

load_dotenv()
model = ChatGoogleGenerativeAI(model="gemini-2.5-flash")

class Review(BaseModel):
    key_themes: list[str] = Field(description="List of key themes in the review")
    summary: str = Field(description="A brief summary of the review")
    sentiment:Literal["positive", "negative", "neutral"] = Field(description="Sentiment of the review")
    pros: Optional[list[str]] = Field(default=None, description="List of pros mentioned in the review")
    cons: Optional[list[str]] = Field(default=None, description="List of cons mentioned in the review")
    name: Optional[str] = Field(default=None, description="Name of the reviewer if mentioned")


structured_model = model.with_structured_output(Review)

result = structured_model.invoke("The product is good but the delivery was late. It has amazing battery life but bulky. John Doe")
print(result)