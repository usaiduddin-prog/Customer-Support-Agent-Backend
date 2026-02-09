import json
from langchain_groq import ChatGroq
from pydantic import ValidationError
from executor.query_plan_schema import QueryPlan
from .prompt import PLANNER_SYSTEM_PROMPT

llm = ChatGroq(
    model="llama-3.1-8b-instant",
    temperature=0
)

def generate_query_plan(user_query: str, max_retries: int = 2) -> QueryPlan:
    messages = [
        {"role": "system", "content": PLANNER_SYSTEM_PROMPT},
        {"role": "user", "content": user_query},
    ]

    for attempt in range(max_retries + 1):
        response = llm.invoke(messages).content

        try:
            data = json.loads(response)
            plan = QueryPlan.model_validate(data)
            return plan

        except (json.JSONDecodeError, ValidationError) as e:
            messages.append({
                "role": "assistant",
                "content": response
            })
            messages.append({
                "role": "user",
                "content": f"""
The previous output was invalid.

Error:
{str(e)}

Fix the JSON and output ONLY valid QueryPlan JSON.
"""
            })

    raise RuntimeError("Failed to generate valid QueryPlan")