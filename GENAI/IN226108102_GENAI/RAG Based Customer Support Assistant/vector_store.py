import os
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_chroma import Chroma

def setup_vector_store(chunks, persist_directory="./chroma_db"):
    """Embeds chunks and stores them in ChromaDB."""
    embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
    vector_store = Chroma.from_documents(
        documents=chunks, 
        embedding=embeddings,
        persist_directory=persist_directory
    )
    return vector_store

def get_retriever(vector_store, k=3):
    """Returns a retriever configured to fetch top_k chunks."""
    return vector_store.as_retriever(search_kwargs={"k": k})
