from tools.product_data import load_data
from typing import Optional
import pandas as pd

def get_customer_summary(customer_id: int):
    df = load_data()
    user_df = df[df["Customer_Id"] == customer_id]

    if user_df.empty:
        return {"error": "Customer not found"}

    return {
        "customer_id": customer_id,
        "total_orders": user_df["order_key"].nunique(),
        "total_items": int(user_df["Quantity"].sum()),
        "total_spent": float(user_df["Sales"].sum()),
        "total_profit": float(user_df["Profit"].sum()),
        "favorite_category": (
            user_df["Product_Category"]
            .value_counts()
            .idxmax()
        )
    }

def get_top_customers(metric: str = "spend", k: int = 5):
    df = load_data()

    metric_map = {
        "spend": "Sales",
        "profit": "Profit",
        "orders": "order_key",
    }

    if metric not in metric_map:
        return {"error": "Invalid metric"}

    if metric == "orders":
        res = (
            df.groupby("Customer_Id")["order_key"]
            .nunique()
            .sort_values(ascending=False)
            .head(k)
        )
    else:
        res = (
            df.groupby("Customer_Id")[metric_map[metric]]
            .sum()
            .sort_values(ascending=False)
            .head(k)
        )

    return res.reset_index().to_dict(orient="records")


def get_customer_behavior(customer_id: int):
    df = load_data()
    user_df = df[df["Customer_Id"] == customer_id]

    if user_df.empty:
        return {"error": "Customer not found"}

    return {
        "customer_id": customer_id,
        "preferred_payment_method": user_df["Payment_method"].value_counts().idxmax(),
        "preferred_device_type": user_df["Device_Type"].value_counts().idxmax(),
        "avg_discount_received": float(user_df["Discount"].mean()),
    }

def get_product_info(product_name: str):
    df = load_data()
    prod_df = df[df["Product"].str.lower() == product_name.lower()]

    if prod_df.empty:
        return {"error": "Product not found"}

    return {
        "product": product_name,
        "total_orders": prod_df["order_key"].nunique(),
        "units_sold": int(prod_df["Quantity"].sum()),
        "total_revenue": float(prod_df["Sales"].sum()),
        "total_profit": float(prod_df["Profit"].sum()),
        "avg_discount": float(prod_df["Discount"].mean()),
        "category": prod_df["Product_Category"].iloc[0]
    }


def get_top_products(metric: str = "revenue", k: int = 5, category: Optional[str] = None):
    df = load_data()

    if category:
        df = df[df["Product_Category"].str.lower() == category.lower()]

    metric_map = {
        "revenue": "Sales",
        "profit": "Profit",
        "units_sold": "Quantity",
    }

    if metric not in metric_map:
        return {"error": "Invalid metric"}

    res = (
        df.groupby("Product")[metric_map[metric]]
        .sum()
        .sort_values(ascending=False)
        .head(k)
    )

    return res.reset_index().to_dict(orient="records")


def get_product_sales_distribution(product_name: str):
    df = load_data()
    prod_df = df[df["Product"].str.lower() == product_name.lower()]

    if prod_df.empty:
        return {"error": "Product not found"}

    return {
        "product": product_name,
        "payment_method_distribution": prod_df["Payment_method"].value_counts().to_dict(),
        "device_type_distribution": prod_df["Device_Type"].value_counts().to_dict(),
        "order_priority_distribution": prod_df["Order_Priority"].value_counts().to_dict(),
    }


def get_category_summary(category_name: str):
    df = load_data()
    cat_df = df[df["Product_Category"].str.lower() == category_name.lower()]

    if cat_df.empty:
        return {"error": "Category not found"}

    return {
        "category": category_name,
        "total_orders": cat_df["order_key"].nunique(),
        "total_units_sold": int(cat_df["Quantity"].sum()),
        "total_revenue": float(cat_df["Sales"].sum()),
        "total_profit": float(cat_df["Profit"].sum()),
        "top_products": (
            cat_df.groupby("Product")["Sales"]
            .sum()
            .sort_values(ascending=False)
            .head(3)
            .index
            .tolist()
        )
    }

def get_best_category(metric: str = "revenue"):
    df = load_data()

    metric_map = {
        "revenue": "Sales",
        "profit": "Profit",
        "units_sold": "Quantity",
    }

    if metric not in metric_map:
        return {"error": "Invalid metric"}

    res = (
        df.groupby("Product_Category")[metric_map[metric]]
        .sum()
        .sort_values(ascending=False)
    )

    return {
        "category": res.index[0],
        "metric": metric,
        "value": float(res.iloc[0]),
    }


def get_category_comparison(metric: str = "revenue"):
    df = load_data()

    metric_map = {
        "revenue": "Sales",
        "profit": "Profit",
        "units_sold": "Quantity",
    }

    if metric not in metric_map:
        return {"error": "Invalid metric"}

    res = (
        df.groupby("Product_Category")[metric_map[metric]]
        .sum()
        .sort_values(ascending=False)
    )

    return res.reset_index().to_dict(orient="records")


def get_sales_summary():
    df = load_data()

    return {
        "total_orders": df["order_key"].nunique(),
        "total_units_sold": int(df["Quantity"].sum()),
        "total_revenue": float(df["Sales"].sum()),
        "total_profit": float(df["Profit"].sum()),
    }


def get_sales_by_date(date: str):
    df = load_data()
    day_df = df[df["Order_Date"] == date]

    if day_df.empty:
        return {"error": "No sales on this date"}

    return {
        "date": date,
        "orders": day_df["order_key"].nunique(),
        "revenue": float(day_df["Sales"].sum()),
        "profit": float(day_df["Profit"].sum()),
    }


def get_sales_trends(group_by: str = "month"):
    df = load_data()

    if "Order_Date" not in df.columns:
        return {"error": "Order_Date column not found"}

    df["Order_Date"] = pd.to_datetime(
        df["Order_Date"], errors="coerce"
    )

    df = df.dropna(subset=["Order_Date"])

    if group_by == "month":
        df["period"] = df["Order_Date"].dt.to_period("M").astype(str)
    elif group_by == "year":
        df["period"] = df["Order_Date"].dt.year
    else:
        return {"error": "Invalid group_by"}

    res = (
        df.groupby("period")[["Sales", "Profit"]]
        .sum()
        .reset_index()
        .rename(columns={"Sales": "revenue", "Profit": "profit"})
    )

    return res.to_dict(orient="records")



def get_payment_method_distribution():
    df = load_data()
    return df["Payment_method"].value_counts().to_dict()


def get_device_type_distribution():
    df = load_data()
    return df["Device_Type"].value_counts().to_dict()


def get_order_priority_distribution():
    df = load_data()
    return df["Order_Priority"].value_counts().to_dict()


def get_discount_impact_analysis():
    df = load_data()

    discounted = df[df["Discount"] > 0]
    non_discounted = df[df["Discount"] == 0]

    return {
        "avg_discount": float(df["Discount"].mean()),
        "avg_profit_with_discount": float(discounted["Profit"].mean()),
        "avg_profit_without_discount": float(non_discounted["Profit"].mean()),
    }


def get_most_discounted_products(k: int = 5):
    df = load_data()

    res = (
        df.groupby("Product")["Discount"]
        .mean()
        .sort_values(ascending=False)
        .head(k)
    )

    return res.reset_index().to_dict(orient="records")