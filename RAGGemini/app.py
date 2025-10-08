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

print("init done \n")

def loadData(filePath):
    return pd.read_excel(filePath)

def dataModeling(combined_texts,embeddings):
    for i in range(len(combined_texts)):
        combined_texts[i] = {"text":combined_texts[i],"embedding":embeddings[i].tolist()}
    
    return combined_texts

def convert_to_embeddings(df, col1, col2):
    combined_texts = (df[col1].astype(str) + " " + df[col2].astype(str)).tolist()
    embeddings = model.encode(combined_texts, show_progress_bar=True)
    return dataModeling(combined_texts,embeddings)

def embed_query(query):
    return model.encode([query])[0].tolist()

def build_contextual_prompt(query, retrieved_docs):
    context = "\n\n".join(retrieved_docs)
    prompt = (
        #"You are a helpful assistant. If the user is greeting, greet back. Use the provided context to answer the user's question. If the context does not contain relevant information, do your best to answer the question using your general knowledge. If you're unsure, say I'm not sure based on the context provided."
        "Ok so injecting the below context is into your memory and always answer in full sentences. U can be the normal chatbot if its outiside of the context and ans the user question. Just greet the user only if he greets you and never mention about the context unless required"
        f"User Question:\n{query}"
        f"Resources:\n{context}\n\n"
    )

    # print(prompt+"\n")
    return prompt

def search_similar_documents(query, top_k=10):
    query_vector = embed_query(query)

    results = collection.aggregate([
        {
            "$vectorSearch": {
                "queryVector": query_vector,
                "path": "embedding",
                "numCandidates": 100,
                "limit": top_k,
                "index": "vector_index"
            }
        }
    ])
 
    return [i["text"] for i in list(results)]


def main():
    while(True):
        message = input("User: ")
        if message == "bye":
            break 

        relevant_docs = search_similar_documents(message)
        prompt = build_contextual_prompt(message, relevant_docs)

        response = chat.send_message_stream(prompt)
        print("Assistant: ", end="")
        
        #response = chat.send_message_stream(message)
        for chunk in response:
            print(chunk.text, end="")



def init():
    df = loadData("/Users/akhilgireesh/Programming/GenAI/RAGGemini/mocksData.xlsx")
    embeddings = convert_to_embeddings(df,"Questions","Answers")
    print(embeddings)
    collection.insert_many(embeddings)
    
main()
#print(search_similar_documents("Hey so who is the current COMPUTER SOCIETY secretary?"))