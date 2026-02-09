from langchain_groq import ChatGroq
from tools.langchain_tools import  sales_summary , sales_trends , customer_summary , product_summary , category_summary
from .query_plan_schema import QueryPlan
from .prompt import ANALYTICS_PRESENTER_PROMPT

TOOL_REGISTRY = {
    "sales_summary": sales_summary,
    "sales_trends": sales_trends,
    "customer_summary": customer_summary,
    "product_summary": product_summary,
    "category_summary": category_summary,
}


def convert_to_human_language(data,user_query: str,plan: QueryPlan): 
    llm = ChatGroq(
        model="llama-3.1-8b-instant",
        temperature=0.2
    )   

    messages = [
        {"role": "system", "content": ANALYTICS_PRESENTER_PROMPT.format(data=data , user_question=user_query , query_plan=plan)},
    ]

    response = llm.invoke(messages).content

    return response




def execute_query_plan(plan: QueryPlan,user_query: str):
    tool_fn = TOOL_REGISTRY.get(plan.tool)

    if not tool_fn:
        raise ValueError(f"Unknown tool: {plan.tool}")

    data =  tool_fn(plan)

    return convert_to_human_language(data,user_query,plan)