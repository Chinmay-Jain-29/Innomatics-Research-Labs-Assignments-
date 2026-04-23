from typing import TypedDict, List
from langgraph.graph import StateGraph, END
from langchain_core.documents import Document
from langchain_groq import ChatGroq

# 1. Define State
class GraphState(TypedDict):
    query: str
    chat_history: str
    retrieved_docs: List[Document]
    answer: str
    confidence: float
    needs_human: bool

def create_workflow(retriever):
    # Initialize LLM
    llm = ChatGroq(model="llama-3.1-8b-instant", temperature=0)
    
    # 2. Define Nodes
    def retrieve_node(state: GraphState):
        query = state["query"]
        docs = retriever.invoke(query)
        return {"retrieved_docs": docs}
        
    def generate_node(state: GraphState):
        query = state["query"]
        docs = state["retrieved_docs"]
        chat_history = state.get("chat_history", "")
        
        context = "\n\n".join([doc.page_content for doc in docs]) if docs else "No background documents found."
        
        prompt = f"""You are an advanced Customer Support AI. 

### Instructions:
1. Use the **Background Knowledge** and **Recent Conversation History** below to answer the user's question.
2. The Background Knowledge may contain snippets from documents OR previously answered questions by human agents (formatted as 'Question: ... Answer: ...').
3. If you find a previously answered question in the Background Knowledge that is the same or very similar to the current User Question, you **MUST** provide that specific Answer.
4. If the answer is not present in the provided context or history, strictly say "I don't know" and nothing else.
5. Do not mention that you are using background knowledge; just provide the answer.

### Background Knowledge (Documents & Memory):
{context}

### Recent Conversation History:
{chat_history}

### User Question:
{query}

Answer:"""
        
        response = llm.invoke(prompt)
        answer = response.content
        
        # Simple confidence heuristic: If model says "I don't know" anywhere, we assume low confidence
        # But we check if it's the STRICT 'I don't know' we asked for.
        if answer.strip().lower() == "i don't know" or "i don't know" in answer.lower():
            confidence = 0.1
        else:
            confidence = 1.0
            
        needs_human = confidence < 0.5
        
        return {"answer": answer, "confidence": confidence, "needs_human": needs_human}
        
    def hitl_node(state: GraphState):
        print("\n[SYSTEM] --- HUMAN IN THE LOOP ESCALATION ---")
        answer = "⚠️ **Escalated to Human Agent:** I'm sorry, I don't know the answer based on the document. \n\n*(Admin: Please use the Admin Panel in the sidebar to reply)*"
        return {"answer": answer, "needs_human": False}

    # 3. Routing Logic
    def route_decision(state: GraphState):
        if state["needs_human"]:
            return "hitl"
        return "output"

    # 4. Build Graph
    workflow = StateGraph(GraphState)
    
    workflow.add_node("retrieve", retrieve_node)
    workflow.add_node("generate", generate_node)
    workflow.add_node("hitl", hitl_node)
    
    workflow.set_entry_point("retrieve")
    workflow.add_edge("retrieve", "generate")
    workflow.add_conditional_edges(
        "generate",
        route_decision,
        {
            "hitl": "hitl",
            "output": END
        }
    )
    workflow.add_edge("hitl", END)
    
    app = workflow.compile()
    return app
