"""
Rate limiting middleware for API endpoints.
Implements in-memory rate limiting to prevent brute force attacks.
"""
import time
from collections import defaultdict
from typing import Dict, Tuple

from fastapi import HTTPException, Request, status
from starlette.middleware.base import BaseHTTPMiddleware


class RateLimitMiddleware(BaseHTTPMiddleware):
    """
    Rate limiting middleware using in-memory storage.
    
    For production, consider using Redis-based rate limiting with slowapi or similar.
    """

    def __init__(self, app):
        super().__init__(app)
        # Storage: {(ip, path): [(timestamp, count), ...]}
        self.requests: Dict[Tuple[str, str], list] = defaultdict(list)
        
        # Rate limits: {path_prefix: (max_requests, window_seconds)}
        self.limits = {
            "/api/auth/login": (5, 60),  # 5 requests per minute
            "/api/auth/register": (3, 3600),  # 3 requests per hour
            "/api/discounts/validate": (10, 60),  # 10 requests per minute
        }

    def _get_client_ip(self, request: Request) -> str:
        """Extract client IP from request."""
        # Check for proxied requests
        forwarded = request.headers.get("X-Forwarded-For")
        if forwarded:
            return forwarded.split(",")[0].strip()
        
        real_ip = request.headers.get("X-Real-IP")
        if real_ip:
            return real_ip
        
        # Fallback to direct client
        if request.client:
            return request.client.host
        return "unknown"

    def _check_rate_limit(self, ip: str, path: str) -> bool:
        """
        Check if request is within rate limit.
        
        Returns True if allowed, False if rate limit exceeded.
        """
        # Find matching rate limit rule
        limit_config = None
        for prefix, config in self.limits.items():
            if path.startswith(prefix):
                limit_config = config
                break
        
        if not limit_config:
            return True  # No rate limit for this path
        
        max_requests, window_seconds = limit_config
        current_time = time.time()
        key = (ip, path)
        
        # Clean old requests outside the window
        self.requests[key] = [
            (timestamp, count) 
            for timestamp, count in self.requests[key]
            if current_time - timestamp < window_seconds
        ]
        
        # Count requests in current window
        total_requests = sum(count for _, count in self.requests[key])
        
        if total_requests >= max_requests:
            return False
        
        # Add current request
        self.requests[key].append((current_time, 1))
        return True

    async def dispatch(self, request: Request, call_next):
        """Process request with rate limiting."""
        client_ip = self._get_client_ip(request)
        path = request.url.path
        
        # Check rate limit
        if not self._check_rate_limit(client_ip, path):
            raise HTTPException(
                status_code=status.HTTP_429_TOO_MANY_REQUESTS,
                detail="Too many requests. Please try again later.",
                headers={"Retry-After": "60"}
            )
        
        response = await call_next(request)
        return response
