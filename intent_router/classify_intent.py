from pydantic import BaseModel, Field
from typing import Literal
from langchain_groq import ChatGroq
from intent_router.prompt import prompt
from dotenv import load_dotenv

load_dotenv()

class IntentClassification(BaseModel):
    intent: Literal["POLICY_QUERY", "ANALYTICS_QUERY", "SMALL_TALK","OUT_OF_SCOPE"] = Field(
        description="Final classified intent"
    )
    confidence: float = Field(
        ge=0.0,
        le=1.0,
        description="Confidence score between 0 and 1"
    )

def get_intent_classifier():
    llm = ChatGroq(
        model="llama-3.1-8b-instant",
        temperature=0.0
    )

    return llm.with_structured_output(IntentClassification)

def classify_intent(query: str) -> IntentClassification:
    classifier = get_intent_classifier()
    chain = prompt | classifier
    return chain.invoke({"query": query})
