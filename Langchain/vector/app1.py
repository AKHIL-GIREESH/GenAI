from langchain_chroma import Chroma
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_huggingface import HuggingFaceEmbeddings
from dotenv import load_dotenv
from langchain_core.documents import Document

load_dotenv()

model = ChatGoogleGenerativeAI(model="gemini-2.5-flash")
embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")

documents = [
    Document(page_content="Artificial Intelligence is transforming the world.", metadata={"source": "AI Overview"}),
    Document(page_content="Machine learning models can learn from data.", metadata={"source": "ML Concepts"}),
    Document(page_content="LangChain helps developers build LLM-powered applications.", metadata={"source": "LangChain Docs"}),
    Document(page_content="Chroma is a vector database for storing embeddings.", metadata={"source": "Chroma Overview"}),
    Document(page_content="Gemini models are developed by Google DeepMind.", metadata={"source": "Gemini Info"}),
]

vectorstore = Chroma(
    embedding_function=embeddings,
    persist_directory="./chroma_db",
    collection_name="sample"
)

vectorstore.add_documents(documents)

query = "What does LangChain help with?"
results = vectorstore.similarity_search(query, k=2)

print(results)

