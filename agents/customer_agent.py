from langchain.agents import AgentExecutor
from langchain.agents.tool_calling_agent import create_tool_calling_agent
from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate
from agents.prompts import SYSTEM_PROMPT
from tools.langchain_tools import (
    customer_summary_tool,
    top_customers_tool,
    customer_behavior_tool,

    product_info_tool,
    top_products_tool,
    product_sales_distribution_tool,

    category_summary_tool,
    best_category_tool,
    category_comparison_tool,

    sales_summary_tool,
    sales_by_date_tool,
    sales_trends_tool,

    payment_method_distribution_tool,
    device_type_distribution_tool,
    order_priority_distribution_tool,
    discount_impact_analysis_tool,
    most_discounted_products_tool,
)
from dotenv import load_dotenv

load_dotenv()

def get_agent():
    llm = ChatGroq(
        model="llama-3.1-8b-instant",
        temperature=0.2,
    )

    tools = [
        customer_summary_tool,
        product_info_tool,
        category_summary_tool,
        top_customers_tool,
        top_products_tool,
        sales_trends_tool,
        best_category_tool,
        sales_by_date_tool,
        sales_summary_tool,
        customer_behavior_tool,
        category_comparison_tool,
        device_type_distribution_tool,
        discount_impact_analysis_tool,
        most_discounted_products_tool,
        product_sales_distribution_tool,
        order_priority_distribution_tool,
        payment_method_distribution_tool,
    ]

    prompt = ChatPromptTemplate.from_messages([
        ("system", SYSTEM_PROMPT),
        ("human", "{input}"),
        ("placeholder", "{agent_scratchpad}")
    ])

    agent = create_tool_calling_agent(
        llm=llm,
        tools=tools,
        prompt=prompt,
    )

    return AgentExecutor(
        agent=agent,
        tools=tools,
        verbose=True,
    )