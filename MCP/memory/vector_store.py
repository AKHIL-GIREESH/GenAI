import chromadb
from sentence_transformers import SentenceTransformer

client = chromadb.Client()
collection = client.get_or_create_collection("memory")
embedder = SentenceTransformer("all-MiniLM-L6-v2")

def store_memory(text: str):
    emb = embedder.encode(text).tolist()
    collection.add(
        documents=[text],
        embeddings=[emb],
        ids=[str(collection.count())]
    )
    return "Memory stored."

def retrieve_memory(query: str, k: int = 3):
    emb = embedder.encode(query).tolist()
    results = collection.query(query_embeddings=[emb], n_results=k)
    return results["documents"][0] if results["documents"] else []
