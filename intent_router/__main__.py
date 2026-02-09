from .classify_intent import classify_intent
from rag.rag_chain import get_rag_chain
from agents.customer_agent import get_agent

rag_chain = get_rag_chain()
agent = get_agent()

def handle_query(query: str) :
    classification = classify_intent(query)

    if classification.intent == "POLICY_QUERY":
        answer, docs = rag_chain(query)
        return {
            "answer": answer,
            "sources": docs
        }

    if classification.intent == "ANALYTICS_QUERY":
        result = agent.invoke({"input": query})
        return {
            "answer": result["output"],
            "sources": None
        }

    return {
        "answer": "Sorry, I can only help with product data and platform policies.",
        "sources": None
    }

