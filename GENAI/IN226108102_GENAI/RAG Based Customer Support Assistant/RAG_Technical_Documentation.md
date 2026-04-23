# 📄 RAG-Based Customer Support Assistant - Technical Documentation

## 1. Introduction

### 1.1 What is Retrieval-Augmented Generation (RAG)
Retrieval-Augmented Generation (RAG) is an AI architecture that combines:
*   **Information Retrieval** (fetching relevant data from a knowledge base)
*   **Text Generation** (using a Large Language Model to generate responses)

Instead of relying solely on pre-trained knowledge, RAG enables the model to:
*   Access external documents (like PDFs)
*   Provide accurate, context-aware responses

### 1.2 Why RAG is Needed
Traditional chatbots:
*   Lack domain-specific knowledge
*   Produce hallucinated answers

RAG solves this by:
*   Grounding responses in real data
*   Improving accuracy and reliability
*   Enabling dynamic knowledge updates

### 1.3 Use Case: Customer Support Assistant
This system simulates a customer support agent that:
*   Reads company documentation (PDF)
*   Answers user queries
*   Escalates to a human when required (HITL - Human-in-the-Loop)

---

## 2. System Architecture

### 2.1 Overview
The system consists of two main pipelines:
1.  **Document Ingestion Pipeline**
2.  **Query Processing Pipeline**

### 2.2 Architecture Components

1.  **User Interface**: CLI or Web interface that accepts user queries.
2.  **Document Loader**: Loads PDF using parsing tools and extracts raw text.
3.  **Chunking Module**: Splits text into smaller chunks while maintaining overlap for context continuity.
4.  **Embedding System**: Converts text into vector representations, enabling similarity-based retrieval.
5.  **Vector Database (ChromaDB)**: Stores embeddings and supports fast similarity search.
6.  **Retrieval Layer**: Fetches top-k relevant chunks based on the query.
7.  **LLM Processing Layer**: Generates answers using the Query + Retrieved context.
8.  **Workflow Engine (LangGraph)**: Controls execution flow, maintains state, and enables branching logic.
9.  **Routing Layer**: Decides the response path (Direct answer vs. Human escalation).
10. **HITL Module**: Handles escalation to a human agent and returns the human response to the user.

### 2.3 Data Flow

**Document Ingestion Pipeline:**
`PDF → Load → Chunk → Embed → Store in ChromaDB`

**Query Processing Pipeline:**
```text
User Query 
    → Embed 
    → Retrieve Chunks 
    → Generate Answer 
    → Evaluate 
        → Return Answer
        → OR Escalate to Human
```

---

## 3. Design Decisions

### 3.1 Chunking Strategy
*   **Chunk Size:** 500–1000 tokens
*   **Overlap:** 100–200 tokens
*   **Reason:** Balances context retention and retrieval efficiency.

### 3.2 Embedding Strategy
*   **Model:** Lightweight transformer embeddings
*   **Reason:** Faster computation and good semantic similarity performance.

### 3.3 Retrieval Approach
*   **Strategy:** Top-k retrieval (k = 3–5) using Cosine similarity search.
*   **Reason:** Ensures relevant context without overloading the LLM.

### 3.4 Prompt Design
**Structure:**
```text
Context:
{retrieved_chunks}

Question:
{user_query}

Answer clearly based on context.
```

---

## 4. Workflow Design (LangGraph)

### 4.1 Nodes
1.  **Input Node:** Accepts user query.
2.  **Processing Node:** Performs Embedding, Retrieval, and Answer generation.
3.  **Decision Node:** Evaluates response quality.
4.  **Output Node:** Returns the final answer.
5.  **HITL Node:** Handles human escalation.

### 4.2 State Object
```python
state = {
    "query": "",
    "retrieved_docs": [],
    "answer": "",
    "confidence": 0.0,
    "needs_human": False
}
```

### 4.3 State Transitions
`Input → Processing → Decision`

**Decision Routing:**
*   `→ Output` (if confident)
*   `→ HITL` (if not confident)

---

## 5. Conditional Logic

### 5.1 Intent Detection
The system evaluates:
*   Query complexity
*   Availability of relevant documents

### 5.2 Routing Criteria
*   **Direct Answer:** Relevant chunks found AND Confidence ≥ threshold.
*   **Escalation:** No relevant data OR Low confidence (< 0.6) OR Ambiguous/complex query.

---

## 6. Human-in-the-Loop (HITL)

### 6.1 When Escalation Happens
*   Retrieval failure
*   Low similarity score
*   Incomplete answer generation

### 6.2 Workflow
`User Query → System → Human → Response → User`

### 6.3 Integration Strategy
*   Simple CLI input for human (Current)
*   Dashboard or ticket system (Future)

### 6.4 Benefits
*   Ensures reliability
*   Handles edge cases
*   Improves trust

### 6.5 Limitations
*   Increased response time
*   Requires human availability

---

## 7. Low-Level Design

### 7.1 Modules
*   **Document Processing Module:** Loads and extracts text.
*   **Chunking Module:** Splits text.
*   **Embedding Module:** Converts text to vectors.
*   **Vector Storage Module:** Stores and retrieves embeddings.
*   **Retrieval Module:** Finds relevant chunks.
*   **Query Processing Module:** Generates response.
*   **Graph Execution Module:** Executes workflow.
*   **HITL Module:** Handles escalation.

### 7.2 Data Structures

**Chunk Format:**
```json
{
  "chunk_id": "c1",
  "text": "...",
  "embedding": [0.1, 0.2, "..."]
}
```

**Query Response:**
```json
{
  "answer": "...",
  "confidence": 0.75,
  "source": "AI/Human"
}
```

---

## 8. Error Handling
*   **Missing PDF:** System alert
*   **No chunks found:** Fallback message
*   **LLM failure:** Retry or escalate

---

## 9. Scalability Considerations

### 9.1 Large Documents
*   Use efficient chunking and indexing.

### 9.2 High Query Load
*   Caching frequent queries.
*   Parallel processing.

### 9.3 Latency
*   Optimize embedding calls.
*   Reduce chunk size if needed.

---

## 10. Testing Strategy

### 10.1 Functional Testing
**Sample Queries:**
*   “What is the refund policy?”
*   “How to cancel a subscription?”

### 10.2 Edge Cases
*   Irrelevant queries
*   Empty queries
*   Complex multi-part questions

### 10.3 Evaluation Metrics
*   Accuracy
*   Response time
*   Escalation rate

---

## 11. Challenges & Trade-offs

### 11.1 Retrieval vs Accuracy
*   More chunks → better context but slower.

### 11.2 Chunk Size vs Context
*   Large chunks → better meaning.
*   Small chunks → faster retrieval.

### 11.3 Cost vs Performance
*   Better LLM → higher cost.

---

## 12. Future Enhancements
*   Multi-document (Multi-PDF) support
*   Chat memory (conversation history)
*   Feedback learning loop
*   Web deployment (AWS/GCP)
*   Fine-tuned embeddings and models

---

# 🧠 1. SYSTEM OVERVIEW (What you are building)

A RAG-based Customer Support Assistant that:
*   Reads company knowledge from PDF
*   Retrieves relevant info using embeddings
*   Answers user queries using LLM
*   Uses LangGraph for decision-making
*   Escalates to human if needed (HITL)

---

# 🏗️ 2. HIGH-LEVEL DESIGN (HLD)

### 🔷 Architecture Components
```text
User (CLI/Web)
      ↓
Query Interface
      ↓
LangGraph Workflow Engine
      ↓
-------------------------------
|  Query Processing Layer     |
|  - Embedding Generator      |
|  - Retriever (ChromaDB)     |
-------------------------------
      ↓
LLM (Answer Generator)
      ↓
Routing Layer (Decision Engine)
      ↓
-------------------------------
|  Response OR HITL Module    |
-------------------------------
      ↓
Final Output to User
```

### 🔷 Document Ingestion Pipeline
`PDF → Loader → Chunking → Embeddings → ChromaDB`

### 🔷 Component Explanation
1.  **Document Loader:** Reads PDF using `PyPDFLoader` and extracts text.
2.  **Chunking Strategy:** Split into chunks (e.g., 500–1000 tokens) with overlap (100–200 tokens).
3.  **Embedding Model:** Converts text → vectors (e.g., OpenAI embeddings, HuggingFace `all-MiniLM-L6-v2`).
4.  **Vector Store (ChromaDB):** Stores embeddings and enables similarity search.
5.  **Retriever:** Takes query → finds top-k relevant chunks.
6.  **LLM:** Generates answer using Query + Retrieved context.
7.  **LangGraph Workflow Engine:** Controls flow of execution, maintains state, applies conditional routing.
8.  **Routing Layer:** Decides to answer directly OR escalate to human.
9.  **HITL Module:** Human takes over when confidence is low, info is missing, or query is complex.

### 🔷 Data Flow (End-to-End)
**Ingestion:** `PDF → Chunk → Embed → Store`

**Querying:**
```text
User Query 
    → Embed Query 
    → Retrieve Chunks 
    → Send to LLM 
    → Generate Answer 
    → Evaluate Answer
        If good → Return
        If bad → HITL → Return human response
```

### 🔷 Technology Choices
*   **ChromaDB:** Lightweight, easy local vector DB.
*   **LangGraph:** Supports workflow + state + branching.
*   **LLM:** OpenAI / LLaMA / Gemini.
*   **Python + LangChain:** Easy integration.

### 🔷 Scalability Considerations
*   Use batching for embeddings.
*   Cache frequent queries.
*   Use better retrievers (FAISS for large scale).
*   Async processing for latency.

---

# ⚙️ 3. LOW-LEVEL DESIGN (LLD)

### 🔷 Module-Level Design
1.  **Document Processing Module:** `load_pdf(file_path) → raw_text`
2.  **Chunking Module:** `chunk_text(text) → list_of_chunks`
3.  **Embedding Module:** `generate_embeddings(chunks) → vectors`
4.  **Vector Storage Module:** `store_embeddings(vectors)`, `retrieve(query_vector) → top_chunks`
5.  **Retrieval Module:** `get_relevant_chunks(query) → context`
6.  **Query Processing Module:** `process_query(query) → answer`
7.  **Graph Execution Module (LangGraph):** Handles Nodes, State, and Routing.
8.  **HITL Module:** `escalate_to_human(query) → human_response`

### 🔷 Data Structures
**Document**
```json
{
  "doc_id": "123",
  "text": "full content"
}
```

**Chunk**
```json
{
  "chunk_id": "c1",
  "text": "...",
  "embedding": [0.12, 0.98]
}
```

**Query State (for LangGraph)**
```python
state = {
    "query": "",
    "retrieved_docs": [],
    "answer": "",
    "confidence": 0.0,
    "needs_human": False
}
```

### 🔷 LangGraph Workflow Design
**Nodes:**
*   **Input Node:** Takes user query.
*   **Processing Node:** Retrieve + generate answer.
*   **Decision Node:** Check confidence.
*   **Output Node:** Return answer.
*   **HITL Node:** Human response.

**Graph Flow:**
```text
Input
  ↓
Process
  ↓
Decision
  ↓            ↓
Output       HITL
```

### 🔷 Conditional Routing Logic
**Conditions for escalation:**
*   No chunks retrieved.
*   Low similarity score.
*   Answer contains: "I don't know" or "Not found".
*   Query too complex.

**Example logic:**
```python
if confidence < 0.6 or not retrieved_docs:
    needs_human = True
```

### 🔷 HITL Design
*   **Trigger:** Confidence low.
*   **Flow:** System → Human → Response → User.
*   **Implementation:** CLI input from human OR API endpoint.

### 🔷 API Design
**Input:**
```json
{
  "query": "What is refund policy?"
}
```
**Output:**
```json
{
  "answer": "...",
  "source": "AI/Human",
  "confidence": 0.78
}
```

### 🔷 Error Handling
*   No PDF loaded → raise error.
*   No chunks found → fallback message.
*   LLM failure → retry or escalate.

---

# 🔄 4. WORKFLOW EXPLANATION (LangGraph Logic)
**Step-by-step execution:**
1.  User inputs query
2.  Query embedded
3.  Retrieve relevant chunks
4.  LLM generates answer
5.  Evaluate answer quality
6.  Route:
    *   Good → Output
    *   Bad → HITL

---

# 🛠️ 5. STEP-BY-STEP BUILD PLAN

### 🔹 Phase 1: Setup
*   Install: `pip install langchain chromadb langgraph openai pypdf`

### 🔹 Phase 2: PDF Pipeline
*   Load PDF
*   Chunk it
*   Generate embeddings
*   Store in ChromaDB

### 🔹 Phase 3: RAG Pipeline
*   Query → embedding
*   Retrieve chunks
*   Send to LLM

### 🔹 Phase 4: Add LangGraph
*   Define state
*   Create nodes
*   Add edges
*   Add conditional routing

### 🔹 Phase 5: Add HITL
*   Add fallback node
*   Take manual input

### 🔹 Phase 6: UI (optional)
*   CLI OR simple React frontend

---

# ⚖️ 6. DESIGN DECISIONS
*   **Chunk size:** Balance context vs performance.
*   **Top-k retrieval:** Usually 3–5.
*   **Embedding model choice.**
*   **Prompt design:** Context + question.

---

# ⚠️ 7. CHALLengeS
*   Wrong retrieval.
*   Hallucination.
*   Latency.
*   Cost of LLM.

---

# 🚀 8. FUTURE ENHANCEMENTS
*   Multi-PDF support
*   Memory (chat history)
*   Feedback loop
*   Fine-tuned embeddings
*   Deployment (AWS/GCP)
