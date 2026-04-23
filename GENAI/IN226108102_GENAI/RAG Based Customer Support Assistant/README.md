# 🧠 RAG-Powered AI Customer Support Assistant

[![Python](https://img.shields.io/badge/Python-3.9+-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://www.python.org/)
[![Streamlit](https://img.shields.io/badge/Streamlit-FF4B4B?style=for-the-badge&logo=Streamlit&logoColor=white)](https://streamlit.io/)
[![LangChain](https://img.shields.io/badge/LangChain-121212?style=for-the-badge&logo=chainlink&logoColor=white)](https://langchain.com/)
[![Groq](https://img.shields.io/badge/Groq-f3d141?style=for-the-badge&logo=lightning&logoColor=black)](https://groq.com/)

A state-of-the-art **RAG (Retrieval-Augmented Generation)** Customer Support Assistant built with **LangGraph**, **Groq (Llama 3.1)**, and **ChromaDB**. This assistant doesn't just answer questions from documents—it learns from human intervention, creating a permanent memory of expert knowledge.

---

## ✨ Key Features

- **🚀 Instant Document Ingestion**: Upload any PDF, and the assistant instantly builds a searchable knowledge base using HuggingFace embeddings.
- **🔄 Agentic Workflow**: Powered by **LangGraph**, the system uses a smart retrieval-generation loop to ensure high-accuracy responses.
- **🛡️ Human-in-the-Loop (HITL)**: When the AI is unsure, it automatically escalates the query to a human agent instead of hallucinating.
- **🧠 Permanent Learning (Memory)**: Human agent responses are saved back into the Vector Database, allowing the AI to answer similar questions correctly in the future.
- **🎨 Premium Glossy UI**: A beautiful, modern Streamlit interface with glassmorphism effects and dynamic animations.

---

## 🛠️ Tech Stack

- **Frontend**: Streamlit (Custom CSS for Glossy UI)
- **Orchestration**: LangGraph (State Machine Logic)
- **LLM**: Groq (Llama 3.1 8B Instant)
- **Vector Database**: ChromaDB
- **Embeddings**: HuggingFace (`all-MiniLM-L6-v2`)
- **Document Processing**: PyPDFLoader & RecursiveCharacterTextSplitter

---

## 🚀 Getting Started

### 1. Prerequisites
- Python 3.9 or higher
- A **Groq API Key** (Get it at [console.groq.com](https://console.groq.com/))

### 2. Installation
Clone the repository and install the dependencies:

```bash
git clone https://github.com/Chinmay-Jain-29/Innomatics-Research-Labs-Assignments-.git
cd "RAG Based Customer Support Assistant"
pip install -r requirements.txt
```

### 3. Environment Setup
Create a `.env` file in the root directory and add your Groq API key:
```env
GROQ_API_KEY=your_api_key_here
```

### 4. Run the Application
```bash
streamlit run app.py
```

---

## 📖 How to Use

1.  **Upload Knowledge**: Use the sidebar to upload a PDF (e.g., Company Policy, Product Manual).
2.  **Process**: Click **"Process Document"** to initialize the AI's brain.
3.  **Chat**: Ask questions in the chat interface.
4.  **Admin Intervention**: 
    - If the AI can't find an answer, it will trigger an **Escalation**.
    - Go to the **Admin Escalation** panel in the sidebar.
    - Provide the correct answer and click **"Submit & Save to Memory"**.
    - The AI now "knows" this answer and will use it for all future similar queries!

---

## 📁 Project Structure

```text
├── app.py                # Main Streamlit Application & UI
├── workflow.py           # LangGraph State Machine & LLM Logic
├── vector_store.py       # ChromaDB Setup & Retrieval logic
├── document_processor.py # PDF Parsing & Chunking
├── requirements.txt      # Project Dependencies
└── .env                  # API Configurations (Hidden)
```

---

## 🛡️ License
Distributed under the MIT License. See `LICENSE` for more information.

---

## 🤝 Contributing
Contributions are what make the open-source community such an amazing place to learn, inspire, and create. Any contributions you make are **greatly appreciated**.

1. Fork the Project
2. Create your Feature Branch (`git checkout -b feature/AmazingFeature`)
3. Commit your Changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the Branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

---

**Developed with ❤️ by [Chinmay Jain](https://github.com/Chinmay-Jain-29)**
