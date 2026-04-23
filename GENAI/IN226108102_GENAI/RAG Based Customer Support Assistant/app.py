import streamlit as st
import os
import tempfile
from dotenv import load_dotenv
from langchain_core.documents import Document

# Load env variables
load_dotenv()

from document_processor import load_and_chunk_pdf
from vector_store import setup_vector_store, get_retriever
from workflow import create_workflow

# Configure page
st.set_page_config(page_title="RAG Assistant", page_icon="✨", layout="wide")

# Custom Glossy UI CSS
st.markdown("""
<style>
    /* Global Font */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600&display=swap');
    html, body, [class*="css"]  {
        font-family: 'Inter', sans-serif;
    }
    
    /* Main Background & Text */
    .stApp {
        background: linear-gradient(135deg, #0f172a 0%, #1e1b4b 100%);
        color: #e2e8f0;
    }
    
    /* Sidebar Glossy Effect */
    [data-testid="stSidebar"] {
        background: rgba(30, 41, 59, 0.7) !important;
        backdrop-filter: blur(16px) !important;
        -webkit-backdrop-filter: blur(16px) !important;
        border-right: 1px solid rgba(255, 255, 255, 0.1) !important;
    }
    
    /* Chat Message Bubbles */
    .stChatMessage {
        background: rgba(255, 255, 255, 0.05);
        border-radius: 12px;
        padding: 10px;
        border: 1px solid rgba(255, 255, 255, 0.08);
        margin-bottom: 15px;
    }
    
    /* Buttons */
    div.stButton > button {
        background: linear-gradient(90deg, #3b82f6 0%, #8b5cf6 100%) !important;
        color: white !important;
        border: none !important;
        border-radius: 8px !important;
        font-weight: 600 !important;
        transition: all 0.3s ease !important;
    }
    div.stButton > button:hover {
        transform: scale(1.02);
        box-shadow: 0 4px 15px rgba(139, 92, 246, 0.4) !important;
    }
    
    /* Input Fields */
    .stTextInput>div>div>input, .stTextArea>div>div>textarea {
        background-color: rgba(15, 23, 42, 0.6) !important;
        border: 1px solid rgba(255, 255, 255, 0.2) !important;
        color: white !important;
        border-radius: 8px !important;
    }
    
    /* Headers */
    h1, h2, h3 {
        color: #f8fafc !important;
    }
    
    /* Chat avatars */
    [data-testid="chatAvatarIcon-user"] {
        background-color: #3b82f6;
    }
    [data-testid="chatAvatarIcon-assistant"] {
        background-color: #8b5cf6;
    }
</style>
""", unsafe_allow_html=True)

# Check for API key
if not os.getenv("GROQ_API_KEY"):
    st.error("Error: GROQ_API_KEY environment variable not set. Please add it to your .env file.")
    st.stop()

# Layout
col1, col2 = st.columns([1, 2.5])

with col1:
    st.header("⚙️ System Setup")
    st.markdown("Upload a PDF to build the AI's brain.")
    uploaded_file = st.file_uploader("Upload Knowledge PDF", type=["pdf"])
    
    if st.button("✨ Process Document") and uploaded_file is not None:
        with st.spinner("Processing PDF and creating Embeddings..."):
            with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp_file:
                tmp_file.write(uploaded_file.getvalue())
                tmp_path = tmp_file.name
            
            chunks = load_and_chunk_pdf(tmp_path)
            vector_store = setup_vector_store(chunks)
            retriever = get_retriever(vector_store)
            
            st.session_state.vector_store = vector_store
            st.session_state.app_workflow = create_workflow(retriever)
            st.session_state.chat_history_str = ""
            st.session_state.messages = []
            
            st.success("PDF processed! Brain activated. 🧠")

    st.markdown("---")
    
    st.header("👨‍💻 Admin Escalation")
    st.caption("Teach the AI what it doesn't know. Your answers are saved forever.")
    human_response = st.text_area("Manual Agent Response:", placeholder="Type the correct answer here...")
    if st.button("🚀 Submit & Save to Memory"):
        if "messages" in st.session_state and len(st.session_state.messages) > 0:
            formatted_response = f"🧑‍💼 **[Human Agent]:** {human_response}"
            st.session_state.messages.append({"role": "assistant", "content": formatted_response})
            
            # Find the last user question
            last_user_query = ""
            for msg in reversed(st.session_state.messages):
                if msg["role"] == "user":
                    last_user_query = msg["content"]
                    break
            
            # 1. Save to transient Chat Memory
            st.session_state.chat_history_str += f"Assistant: [Human Response] {human_response}\n\n"
            
            # 2. Add to Vector DB for PERMANENT Memory
            if last_user_query and "vector_store" in st.session_state:
                new_doc = Document(
                    page_content=f"Question: {last_user_query}\nAnswer: {human_response}", 
                    metadata={"source": "human_feedback"}
                )
                st.session_state.vector_store.add_documents([new_doc])
                st.success("✅ Answer sent to user AND saved to Vector Database! The AI will now know this forever.")
            else:
                st.warning("Sent to user, but could not save to Vector DB (not initialized).")
                
            st.rerun()
        else:
            st.error("No active chat to respond to.")

with col2:
    st.header("✨ AI Support Chat")
    
    if "messages" not in st.session_state:
        st.session_state.messages = []
        
    if "chat_history_str" not in st.session_state:
        st.session_state.chat_history_str = ""

    # Display chat
    for msg in st.session_state.messages:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])

    # Chat input
    if prompt := st.chat_input("Ask me anything..."):
        if "app_workflow" not in st.session_state:
            st.warning("Please upload and process a PDF in the sidebar first!")
            st.stop()
            
        # Add user message
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)
            
        with st.spinner("Searching knowledge base..."):
            result = st.session_state.app_workflow.invoke({
                "query": prompt,
                "chat_history": st.session_state.chat_history_str,
                "retrieved_docs": [],
                "answer": "",
                "confidence": 0.0,
                "needs_human": False
            })
            
            answer = result["answer"]
            
            st.session_state.messages.append({"role": "assistant", "content": answer})
            with st.chat_message("assistant"):
                st.markdown(answer)
                
            # Update chat history memory
            st.session_state.chat_history_str += f"User: {prompt}\nAssistant: {answer}\n\n"
