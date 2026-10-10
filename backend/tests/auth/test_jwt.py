"""Tests for JWT token utilities."""
import time

import jwt as pyjwt
import pytest

from app.auth.jwt import create_access_token, decode_access_token
from app.config import settings


def test_create_access_token():
    """Test JWT token creation."""
    customer_id = 123
    role = "shopper"
    
    token = create_access_token(customer_id, role)
    
    # Token should be a non-empty string
    assert isinstance(token, str)
    assert len(token) > 0
    
    # Decode token manually to verify structure
    payload = pyjwt.decode(token, settings.jwt_secret, algorithms=[settings.jwt_algorithm])
    assert payload["sub"] == str(customer_id)
    assert payload["role"] == role
    assert "exp" in payload


def test_decode_access_token_valid():
    """Test decoding a valid JWT token."""
    customer_id = 456
    role = "admin"
    
    token = create_access_token(customer_id, role)
    payload = decode_access_token(token)
    
    assert payload is not None
    assert payload["sub"] == str(customer_id)
    assert payload["role"] == role
    assert "exp" in payload


def test_decode_access_token_invalid():
    """Test decoding an invalid JWT token."""
    invalid_token = "invalid.jwt.token"
    
    payload = decode_access_token(invalid_token)
    
    assert payload is None


def test_decode_access_token_expired():
    """Test decoding an expired JWT token."""
    import datetime
    
    # Create a token that expires immediately
    expire = datetime.datetime.utcnow() - datetime.timedelta(seconds=1)
    payload_data = {
        "sub": "123",
        "role": "shopper",
        "exp": expire
    }
    
    expired_token = pyjwt.encode(payload_data, settings.jwt_secret, algorithm=settings.jwt_algorithm)
    
    # Wait a moment to ensure it's expired
    time.sleep(0.1)
    
    payload = decode_access_token(expired_token)
    
    assert payload is None


def test_token_contains_expiry():
    """Test that created tokens include expiry claim."""
    token = create_access_token(789, "customer_support")
    
    # Decode without verification to check structure
    unverified_payload = pyjwt.decode(
        token,
        options={"verify_signature": False}
    )
    
    assert "exp" in unverified_payload
    
    # Expiry should be in the future
    import datetime
    exp_timestamp = unverified_payload["exp"]
    now_timestamp = datetime.datetime.utcnow().timestamp()
    
    assert exp_timestamp > now_timestamp


def test_different_roles():
    """Test token creation with different roles."""
    roles = ["shopper", "admin", "inventory_manager", "customer_support"]
    
    for role in roles:
        token = create_access_token(100, role)
        payload = decode_access_token(token)
        
        assert payload is not None
        assert payload["role"] == role
