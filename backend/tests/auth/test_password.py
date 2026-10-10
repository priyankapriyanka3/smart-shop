"""Tests for password hashing utilities."""
import pytest

from app.auth.password import hash_password, verify_password


def test_hash_password():
    """Test password hashing."""
    password = "TestPassword123!"
    hashed = hash_password(password)
    
    # Hashed password should be different from plain text
    assert hashed != password
    
    # Hashed password should start with bcrypt prefix
    assert hashed.startswith("$2b$")
    
    # Hash should be deterministic for bcrypt (but different each time due to salt)
    hashed2 = hash_password(password)
    assert hashed != hashed2  # Different due to random salt


def test_verify_password_correct():
    """Test password verification with correct password."""
    password = "CorrectPassword123!"
    hashed = hash_password(password)
    
    assert verify_password(password, hashed) is True


def test_verify_password_incorrect():
    """Test password verification with incorrect password."""
    password = "CorrectPassword123!"
    hashed = hash_password(password)
    
    assert verify_password("WrongPassword456!", hashed) is False


def test_verify_password_empty():
    """Test password verification with empty password."""
    password = "TestPassword123!"
    hashed = hash_password(password)
    
    assert verify_password("", hashed) is False


def test_hash_different_passwords():
    """Test that different passwords produce different hashes."""
    password1 = "Password1!"
    password2 = "Password2!"
    
    hash1 = hash_password(password1)
    hash2 = hash_password(password2)
    
    assert hash1 != hash2
