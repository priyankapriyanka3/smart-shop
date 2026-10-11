"""Rate limiting middleware for authentication endpoints."""
from typing import Dict, Tuple
from datetime import datetime, timedelta
from fastapi import Request, Response, status
from fastapi.responses import JSONResponse
from starlette.middleware.base import BaseHTTPMiddleware
import json


class RateLimitMiddleware(BaseHTTPMiddleware):
    """
    Rate limiting middleware for login endpoint.
    
    Limits: 5 attempts per email per 15 minutes (configurable).
    Tracks attempts by email address from request body.
    """
    
    def __init__(self, app, max_attempts: int = 5, window_minutes: int = 15):
        """
        Initialize rate limiter.
        
        Args:
            app: FastAPI application
            max_attempts: Maximum login attempts per email per window
            window_minutes: Time window in minutes
        """
        super().__init__(app)
        self.max_attempts = max_attempts
        self.window = timedelta(minutes=window_minutes)
        # In-memory storage: email -> [(timestamp, success), ...]
        # For production, use Redis or similar distributed cache
        self._attempts: Dict[str, list] = {}
    
    async def dispatch(self, request: Request, call_next):
        """
        Process request and apply rate limiting to login endpoint.
        
        Args:
            request: FastAPI request
            call_next: Next middleware/route handler
        
        Returns:
            Response with 429 if rate limited, otherwise normal response
        """
        # Skip rate limiting during tests
        import os
        if os.getenv("TESTING") == "1":
            return await call_next(request)
        
        # Only apply rate limiting to login endpoint
        if request.url.path == "/api/v1/auth/login" and request.method == "POST":
            # Read request body to extract email
            body = await request.body()
            
            # Parse email from JSON body
            try:
                data = json.loads(body.decode("utf-8"))
                email = data.get("email", "").lower()
            except (json.JSONDecodeError, UnicodeDecodeError):
                # Invalid JSON, let the route handler deal with it
                # Restore body for route handler
                async def receive():
                    return {"type": "http.request", "body": body}
                request._receive = receive
                return await call_next(request)
            
            # Check rate limit for this email
            if self._is_rate_limited(email):
                return JSONResponse(
                    status_code=status.HTTP_429_TOO_MANY_REQUESTS,
                    content={
                        "detail": "Too many login attempts. Please try again later.",
                        "status_code": 429,
                    },
                    headers={
                        "Retry-After": str(self.window.total_seconds()),
                    },
                )
            
            # Restore body for route handler
            async def receive():
                return {"type": "http.request", "body": body}
            request._receive = receive
            
            # Process request
            response = await call_next(request)
            
            # Record attempt after processing (to know if it was successful)
            # For simplicity, we record all attempts as failures initially
            # A more sophisticated implementation would check response status
            self._record_attempt(email, success=(response.status_code == 200))
            
            return response
        
        # Not a login endpoint, pass through
        return await call_next(request)
    
    def _is_rate_limited(self, email: str) -> bool:
        """
        Check if email has exceeded rate limit.
        
        Args:
            email: Email address (lowercase)
        
        Returns:
            True if rate limited, False otherwise
        """
        if not email:
            return False
        
        now = datetime.utcnow()
        
        # Clean up old attempts
        if email in self._attempts:
            self._attempts[email] = [
                (ts, success) for ts, success in self._attempts[email]
                if now - ts < self.window
            ]
            
            # Count failed attempts in window
            failed_attempts = sum(
                1 for ts, success in self._attempts[email]
                if not success
            )
            
            if failed_attempts >= self.max_attempts:
                return True
        
        return False
    
    def _record_attempt(self, email: str, success: bool):
        """
        Record login attempt for email.
        
        Args:
            email: Email address (lowercase)
            success: Whether login was successful
        """
        if not email:
            return
        
        now = datetime.utcnow()
        
        if email not in self._attempts:
            self._attempts[email] = []
        
        self._attempts[email].append((now, success))
        
        # Clean up old attempts
        self._attempts[email] = [
            (ts, s) for ts, s in self._attempts[email]
            if now - ts < self.window
        ]
    
    def reset_attempts(self, email: str):
        """
        Reset rate limit for email (for testing).
        
        Args:
            email: Email address to reset
        """
        email_lower = email.lower()
        if email_lower in self._attempts:
            del self._attempts[email_lower]
