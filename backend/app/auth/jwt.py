"""
JWT token generation and validation utilities.
"""
from datetime import datetime, timedelta

import jwt

from app.config import settings


def create_access_token(customer_id: int, role: str) -> str:
    """
    Create a JWT access token.

    Args:
        customer_id: Customer ID to embed in token
        role: User role (shopper, admin, inventory_manager, customer_support)

    Returns:
        JWT token string
    """
    expire = datetime.utcnow() + timedelta(hours=settings.jwt_expiration_hours)
    payload = {
        "sub": str(customer_id),  # Convert to string for JWT standard
        "role": role,
        "exp": expire
    }
    return jwt.encode(payload, settings.jwt_secret, algorithm=settings.jwt_algorithm)


def decode_access_token(token: str) -> dict | None:
    """
    Decode and validate a JWT access token.

    Args:
        token: JWT token string

    Returns:
        Decoded payload dict if valid, None if invalid or expired
    """
    try:
        payload = jwt.decode(
            token,
            settings.jwt_secret,
            algorithms=[settings.jwt_algorithm]
        )
        return payload
    except jwt.ExpiredSignatureError:
        return None
    except jwt.InvalidTokenError:
        return None
