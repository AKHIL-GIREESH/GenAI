from langchain_ollama import ChatOllama, OllamaEmbeddings
from langchain_core.messages import SystemMessage, HumanMessage, AIMessage
from dotenv import load_dotenv
from langchain_chroma import Chroma

load_dotenv()
model = ChatOllama(model="mistral:7b", temperature=0)
embeddings = OllamaEmbeddings(model="mistral:7b")

vector_db = Chroma(
    collection_name="user_memory",
    embedding_function=embeddings,
    host="localhost",
    port=8000
)

if vector_db._collection.count() == 0:
    print("Adding facts to memory...")
    facts = ["name is John Doe", "Country is India", "Is a student"]
    vector_db.add_texts(texts=facts, ids=["fact1", "fact2", "fact3"])

chatHistory = [
    SystemMessage(content="You are a human friend with personality type ESTP")
]

while True:
    userInput = input("User: ")
    if userInput == "bye":
        break

    docs = vector_db.similarity_search(userInput, k=2)
    context = "\n".join([d.page_content for d in docs])

    rag_input = f"Context from memory:\n{context}\n\nUser Question: {userInput}"
    
    chatHistory.append(HumanMessage(content=rag_input))
    result = model.invoke(chatHistory)
    chatHistory.append(AIMessage(content=result.content))
    print("AI:", result.content)
