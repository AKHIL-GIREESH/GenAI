from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI


load_dotenv()
model = ChatGoogleGenerativeAI(model="gemini-2.5-flash")


json_schema = {
  "title": "Review",
  "type": "object",
  "properties": {
    "key_themes": {
      "type": "array",
      "items": { "type": "string" },
      "description": "List of key themes in the review"
    },
    "summary": {
      "type": "string",
      "description": "A brief summary of the review"
    },
    "sentiment": {
      "type": "string",
      "enum": ["positive", "negative", "neutral"],
      "description": "Sentiment of the review"
    },
    "pros": {
      "type": ["array", "null"],
      "items": { "type": "string" },
      "description": "List of pros mentioned in the review"
    },
    "cons": {
      "type": ["array", "null"],
      "items": { "type": "string" },
      "description": "List of cons mentioned in the review"
    },
    "name": {
      "type": ["string", "null"],
      "description": "Name of the reviewer if mentioned"
    }
  },
  "required": ["key_themes", "summary", "sentiment"]
}


structured_model = model.with_structured_output(json_schema)

result = structured_model.invoke("The product is good but the delivery was late. It has amazing battery life but bulky. John Doe")
print(result)