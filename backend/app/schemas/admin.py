"""Admin domain schemas: Dashboard statistics and metrics."""
from typing import List
from pydantic import BaseModel


class StatsResponse(BaseModel):
    """Statistics card for admin dashboard."""
    label: str
    value: str | int | float
    trend: str | None = None  # positive, negative, neutral
    trend_value: str | None = None


class DashboardResponse(BaseModel):
    """Admin dashboard response."""
    stats: List[StatsResponse]
    low_stock_count: int
    pending_orders_count: int
    pending_reviews_count: int
