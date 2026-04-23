import os
import time
from dotenv import load_dotenv

# Load environment variables first
load_dotenv()

from document_processor import load_and_chunk_pdf
from vector_store import setup_vector_store, get_retriever
from workflow import create_workflow

def main():
    print("="*50)
    print(" RAG-Based Customer Support Assistant ")
    print("="*50)
    
    # Check for API Key
    if not os.getenv("GROQ_API_KEY"):
        print("Error: GROQ_API_KEY environment variable not set.")
        print("Please copy .env.example to .env and add your Groq API key.")
        return
        
    pdf_path = "sample_knowledge.pdf"
    
    if not os.path.exists(pdf_path):
        print(f"Warning: Could not find '{pdf_path}'.")
        print("Please run 'python create_sample_pdf.py' to generate a sample PDF first.")
        return
        
    print("[1/3] Loading and indexing PDF...")
    start_time = time.time()
    chunks = load_and_chunk_pdf(pdf_path)
    print(f"      Created {len(chunks)} chunks.")
    
    print("[2/3] Setting up Vector Store (ChromaDB)...")
    vector_store = setup_vector_store(chunks)
    retriever = get_retriever(vector_store)
    
    print("[3/3] Initializing LangGraph Workflow...")
    app = create_workflow(retriever)
    
    print(f"\nSystem ready in {time.time() - start_time:.2f} seconds!")
    print("Type 'exit' or 'quit' to stop.")
    
    chat_history_str = ""
    
    while True:
        query = input("\nUser Query: ")
        if query.lower() in ['exit', 'quit']:
            break
            
        if not query.strip():
            continue
            
        # Run workflow
        result = app.invoke({
            "query": query, 
            "chat_history": chat_history_str,
            "retrieved_docs": [], 
            "answer": "", 
            "confidence": 0.0, 
            "needs_human": False
        })
        
        answer = result['answer']
        print(f"\nAssistant: {answer}")
        
        # Append to memory for the next loop
        chat_history_str += f"User: {query}\nAssistant: {answer}\n\n"

if __name__ == "__main__":
    main()
