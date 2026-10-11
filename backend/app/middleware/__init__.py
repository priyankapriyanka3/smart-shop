"""Middleware module for Smart Shop API."""

from app.middleware.rate_limit import RateLimitMiddleware

__all__ = ["RateLimitMiddleware"]
