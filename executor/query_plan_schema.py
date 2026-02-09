from typing import Literal, Optional, Dict, Any
from pydantic import BaseModel, Field, model_validator
from data.constants import ALLOWED_FILTER_COLUMNS

class QueryPlan(BaseModel):
    tool: Literal[
        "sales_summary",
        "sales_trends",
        "customer_summary",
        "product_summary",
        "category_summary",
        "none"
    ]

    filters: Optional[Dict[str, Any]] = None

    date_range: Optional[Dict[str, str]] = Field(
        default=None,
        description="{'from': 'YYYY-MM-DD', 'to': 'YYYY-MM-DD'}"
    )

    limit: int = 20

    @model_validator(mode="before")
    def sanitize_filters(cls, values):
        filters = values.get("filters")

        if not filters:
            return values

        if isinstance(filters, list):
            normalized = {}
            for item in filters:
                if isinstance(item, dict):
                    normalized.update(item)
            filters = normalized or None

        if not isinstance(filters, dict):
            values["filters"] = None
            return values

        cleaned = {
            k: v for k, v in filters.items()
            if k in ALLOWED_FILTER_COLUMNS
        }

        values["filters"] = cleaned or None
        return values