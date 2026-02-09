from .classify_intent import classify_intent
from rag.rag_chain import get_rag_chain
from tools.__main__ import handle_user_query

rag_chain = get_rag_chain()

def handle_query(query: str) :
    classification = classify_intent(query)

    if classification.confidence < 0.6:
        return {
            "answer": "Could you please clarify your question? I want to help accurately 🙂",
            "sources": None
        }

    if classification.intent == "SMALL_TALK":
        return {
            "answer": "Hi! 👋 How can I help you with your orders or policies today?",
            "sources": None
        }

    if classification.intent == "POLICY_QUERY":
        answer, docs = rag_chain(query)
        return {
            "answer": answer,
            "sources": docs
        }

    if classification.intent == "ANALYTICS_QUERY":
        return {
            "answer": handle_user_query(query),
            "sources": None
        }

    return {
        "answer": "Sorry, I can only help with product data and platform policies.",
        "sources": None
    }

