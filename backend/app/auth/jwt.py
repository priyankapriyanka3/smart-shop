"""JWT token creation and verification using PyJWT."""
from datetime import datetime, timedelta
from typing import Optional
import jwt
from app.config import settings


def create_access_token(user_id: int, expires_delta: Optional[timedelta] = None) -> str:
    """
    Create JWT access token with exp claim.
    
    Args:
        user_id: Integer user ID (User.id must be Integer)
        expires_delta: Optional custom expiration time
    
    Returns:
        JWT token string
    """
    if expires_delta is None:
        expires_delta = timedelta(minutes=settings.access_token_expire_minutes)
    
    expire = datetime.utcnow() + expires_delta
    
    # JWT payload embeds str(user.id) as required by architecture contract
    payload = {
        "sub": str(user_id),
        "exp": expire,
        "iat": datetime.utcnow(),
    }
    
    token = jwt.encode(payload, settings.secret_key, algorithm=settings.algorithm)
    return token


def decode_access_token(token: str) -> Optional[dict]:
    """
    Decode and verify JWT access token.
    
    Args:
        token: JWT token string
    
    Returns:
        Decoded payload dict if valid, None otherwise
    """
    try:
        payload = jwt.decode(
            token,
            settings.secret_key,
            algorithms=[settings.algorithm],
        )
        return payload
    except jwt.ExpiredSignatureError:
        # Token has expired
        return None
    except jwt.InvalidTokenError:
        # Token is invalid
        return None
