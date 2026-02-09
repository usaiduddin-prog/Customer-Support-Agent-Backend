from planner.planner import generate_query_plan
from executor.query_executor import execute_query_plan

def handle_user_query(user_query: str):
    plan = generate_query_plan(user_query)

    if plan.tool == "none":
        return "I can help with ecommerce analytics questions only."

    return execute_query_plan(plan,user_query)