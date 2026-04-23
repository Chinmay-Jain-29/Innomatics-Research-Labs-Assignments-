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
        
        prompt = f"""You are a helpful customer support assistant.

Background Knowledge:
{context}

Recent Conversation History:
{chat_history}

User Question:
{query}

Answer clearly based ONLY on the Background Knowledge and Recent Conversation History. If you cannot answer based on these, strictly say "I don't know"."""
        
        response = llm.invoke(prompt)
        answer = response.content
        
        # Simple confidence heuristic
        confidence = 0.9 if "I don't know" not in answer else 0.1
        needs_human = confidence < 0.6
        
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
