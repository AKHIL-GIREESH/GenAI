import os
import pandas as pd # type: ignore
from google import genai
from dotenv import load_dotenv # type: ignore
from pymongo import MongoClient # type: ignore
from sentence_transformers import SentenceTransformer # type: ignore

load_dotenv()

model = SentenceTransformer("all-MiniLM-L6-v2")

client = genai.Client(api_key= os.getenv("GEMINI_API_KEY"))
chat = client.chats.create(model="gemini-2.0-flash")

clientdb = MongoClient(os.getenv("MONGODB_URI"))
db = clientdb["GenAI"]
collection = db["test0"]



def loadData(filePath):
    return pd.read_excel(filePath)

def convert_to_embeddings(df, col1, col2):
    combined_texts = (df[col1].astype(str) + " " + df[col2].astype(str)).tolist()
    embeddings = model.encode(combined_texts, show_progress_bar=True)
    return embeddings


def main():
    while(True):
        message = input("User: ")
        if message == "bye":
            break 
        
        response = chat.send_message_stream(message)
        for chunk in response:
            print(chunk.text, end="")

df = loadData("/Users/akhilgireesh/Programming/GenAI/RAGGemini/mocksData.xlsx")
embeddings = convert_to_embeddings(df,"Questions","Answers")
print(embeddings)
#main()