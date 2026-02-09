from langchain_core.tools import tool
from typing import Optional

from tools.product_tools import (
    get_customer_summary,
    get_top_customers,
    get_customer_behavior,

    get_product_info,
    get_top_products,
    get_product_sales_distribution,

    get_category_summary,
    get_best_category,
    get_category_comparison,

    get_sales_summary,
    get_sales_by_date,
    get_sales_trends,

    get_payment_method_distribution,
    get_device_type_distribution,
    get_order_priority_distribution,

    get_discount_impact_analysis,
    get_most_discounted_products,
)



@tool
def customer_summary_tool(customer_id: int):
    """Get total orders, items bought, spending, profit, and favorite category for a customer."""
    return get_customer_summary(customer_id)


@tool
def top_customers_tool(metric: str = "spend", k: int = 5):
    """
    Get top customers by metric.
    metric: spend | profit | orders
    """
    return get_top_customers(metric, k)


@tool
def customer_behavior_tool(customer_id: int):
    """Get customer preferences like payment method, device type, and average discount."""
    return get_customer_behavior(customer_id)



@tool
def product_info_tool(product_name: str):
    """Get sales, revenue, profit, discount, and category info for a product."""
    return get_product_info(product_name)


@tool
def top_products_tool(metric: str = "revenue", k: int = 5, category: Optional[str] = None):
    """
    Get top products by revenue, profit, or units sold.
    Optionally filter by category.
    """
    return get_top_products(metric, k, category)


@tool
def product_sales_distribution_tool(product_name: str):
    """Get payment method, device type, and order priority distribution for a product."""
    return get_product_sales_distribution(product_name)



@tool
def category_summary_tool(category_name: str):
    """Get revenue, profit, units sold, and top products for a category."""
    return get_category_summary(category_name)


@tool
def best_category_tool(metric: str = "revenue"):
    """
    Find the best-performing category.
    metric: revenue | profit | units_sold
    """
    return get_best_category(metric)


@tool
def category_comparison_tool(metric: str = "revenue"):
    """Compare all categories by revenue, profit, or units sold."""
    return get_category_comparison(metric)



@tool
def sales_summary_tool():
    """Get overall sales, orders, units sold, revenue, and profit."""
    return get_sales_summary()


@tool
def sales_by_date_tool(date: str):
    """Get sales and profit for a specific date (YYYY-MM-DD)."""
    return get_sales_by_date(date)


@tool
def sales_trends_tool(group_by: str = "month"):
    """
    Get sales trends grouped by month or year.
    group_by: month | year
    """
    return get_sales_trends(group_by)



@tool
def payment_method_distribution_tool():
    """Get distribution of payment methods across all orders."""
    return get_payment_method_distribution()


@tool
def device_type_distribution_tool():
    """Get distribution of device types used for orders."""
    return get_device_type_distribution()


@tool
def order_priority_distribution_tool():
    """Get distribution of order priority levels."""
    return get_order_priority_distribution()



@tool
def discount_impact_analysis_tool():
    """Analyze how discounts affect profitability."""
    return get_discount_impact_analysis()


@tool
def most_discounted_products_tool(k: int = 5):
    """Get products with the highest average discounts."""
    return get_most_discounted_products(k)