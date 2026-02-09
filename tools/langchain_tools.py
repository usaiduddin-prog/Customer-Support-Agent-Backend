from data.db import run_sql
from executor.query_plan_schema import QueryPlan
from data.helper import build_where_clause

def sales_summary(plan : QueryPlan):
    """
    Get overall orders, revenue, profit, and units sold.
    """
    where_sql, params = build_where_clause(plan.filters, plan.date_range)

    query = f"""
        SELECT
            COUNT(*) AS total_orders,
            SUM(Sales) AS total_sales,
            SUM(Profit) AS total_profit,
            AVG(Discount) AS avg_discount
        FROM orders
        {where_sql}
    """
    return run_sql(query, params)


def sales_trends(plan : QueryPlan):
    """
    Get sales and profit trends grouped by month or year.
    """
    where_sql, params = build_where_clause(plan.filters, plan.date_range)

    query = f"""
        SELECT
            Order_Date,
            SUM(Sales) AS total_sales,
            SUM(Profit) AS total_profit
        FROM orders
        {where_sql}
        GROUP BY Order_Date
        ORDER BY Order_Date ASC
        LIMIT ?
    """

    return run_sql(query, params + (plan.limit,))



def customer_summary(plan : QueryPlan):
    """
    Get customer-level order, spend, profit, and preferences.
    """
    where_sql, params = build_where_clause(plan.filters, plan.date_range)

    query = f"""
        SELECT
            Customer_Id,
            COUNT(*) AS orders_count,
            SUM(Sales) AS total_spent,
            SUM(Profit) AS total_profit
        FROM orders
        {where_sql}
        GROUP BY Customer_Id
        ORDER BY total_spent DESC
        LIMIT ?
    """

    return run_sql(query, params + (plan.limit,))


def product_summary(plan : QueryPlan):
    """
    Get product sales, revenue, profit, discount, and category.
    """
    where_sql, params = build_where_clause(plan.filters, plan.date_range)

    query = f"""
        SELECT
            Product,
            SUM(Quantity) AS total_units_sold,
            SUM(Sales) AS total_sales,
            SUM(Profit) AS total_profit
        FROM orders
        {where_sql}
        GROUP BY Product
        ORDER BY total_sales DESC
        LIMIT ?
    """

    return run_sql(query, params + (plan.limit,))



def category_summary(plan : QueryPlan):
    """
    Get category-level performance and top products.
    """
    where_sql, params = build_where_clause(plan.filters, plan.date_range)

    query = f"""
        SELECT
            Product_Category,
            SUM(Sales) AS total_sales,
            SUM(Profit) AS total_profit,
            SUM(Quantity) AS total_units
        FROM orders
        {where_sql}
        GROUP BY Product_Category
        ORDER BY total_sales DESC
        LIMIT ?
    """

    return run_sql(query, params + (plan.limit,))