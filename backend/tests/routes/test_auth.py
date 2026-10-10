"""Tests for authentication routes."""
import pytest

from app.models.customer import Customer


def test_register_success(client):
    """Test successful user registration."""
    response = client.post(
        "/api/auth/register",
        json={
            "email": "newuser@example.com",
            "password": "SecurePass123!",
            "full_name": "New User"
        }
    )
    
    assert response.status_code == 201
    data = response.json()
    
    assert "access_token" in data
    assert data["token_type"] == "bearer"
    assert "user" in data
    assert data["user"]["email"] == "newuser@example.com"
    assert data["user"]["full_name"] == "New User"
    assert data["user"]["role"] == "shopper"
    assert data["user"]["is_active"] is True


def test_register_duplicate_email(client, sample_customer):
    """Test registration with existing email."""
    response = client.post(
        "/api/auth/register",
        json={
            "email": sample_customer.email,
            "password": "AnotherPass123!",
            "full_name": "Duplicate User"
        }
    )
    
    assert response.status_code == 400
    assert "already registered" in response.json()["detail"].lower()


def test_register_weak_password(client):
    """Test registration with weak password."""
    # No uppercase
    response = client.post(
        "/api/auth/register",
        json={
            "email": "weak@example.com",
            "password": "weakpass123",
            "full_name": "Weak User"
        }
    )
    assert response.status_code == 400
    assert "uppercase" in response.json()["detail"].lower()
    
    # No lowercase
    response = client.post(
        "/api/auth/register",
        json={
            "email": "weak2@example.com",
            "password": "WEAKPASS123",
            "full_name": "Weak User 2"
        }
    )
    assert response.status_code == 400
    assert "lowercase" in response.json()["detail"].lower()
    
    # No number
    response = client.post(
        "/api/auth/register",
        json={
            "email": "weak3@example.com",
            "password": "WeakPassword",
            "full_name": "Weak User 3"
        }
    )
    assert response.status_code == 400
    assert "number" in response.json()["detail"].lower()


def test_register_short_password(client):
    """Test registration with too short password."""
    response = client.post(
        "/api/auth/register",
        json={
            "email": "short@example.com",
            "password": "Short1!",  # Only 7 characters
            "full_name": "Short Pass User"
        }
    )
    
    assert response.status_code == 422  # Pydantic validation error


def test_login_success(client, sample_customer):
    """Test successful login."""
    response = client.post(
        "/api/auth/login",
        json={
            "email": sample_customer.email,
            "password": "TestPassword123!"
        }
    )
    
    assert response.status_code == 200
    data = response.json()
    
    assert "access_token" in data
    assert data["token_type"] == "bearer"
    assert "user" in data
    assert data["user"]["email"] == sample_customer.email


def test_login_wrong_password(client, sample_customer):
    """Test login with incorrect password."""
    response = client.post(
        "/api/auth/login",
        json={
            "email": sample_customer.email,
            "password": "WrongPassword123!"
        }
    )
    
    assert response.status_code == 401
    assert "invalid" in response.json()["detail"].lower()


def test_login_nonexistent_user(client):
    """Test login with non-existent email."""
    response = client.post(
        "/api/auth/login",
        json={
            "email": "nonexistent@example.com",
            "password": "SomePassword123!"
        }
    )
    
    assert response.status_code == 401
    assert "invalid" in response.json()["detail"].lower()


def test_get_current_user(client, sample_customer, auth_headers):
    """Test getting current user profile."""
    response = client.get(
        "/api/auth/me",
        headers=auth_headers
    )
    
    assert response.status_code == 200
    data = response.json()
    
    assert data["email"] == sample_customer.email
    assert data["full_name"] == sample_customer.full_name
    assert data["role"] == sample_customer.role


def test_get_current_user_unauthorized(client):
    """Test getting profile without authentication."""
    response = client.get("/api/auth/me")
    
    assert response.status_code == 401  # API returns 401 for missing/invalid auth


def test_get_current_user_invalid_token(client):
    """Test getting profile with invalid token."""
    response = client.get(
        "/api/auth/me",
        headers={"Authorization": "Bearer invalid.jwt.token"}
    )
    
    assert response.status_code == 401


def test_update_profile_full_name(client, sample_customer, auth_headers):
    """Test updating profile full name."""
    response = client.put(
        "/api/auth/profile",
        headers=auth_headers,
        json={
            "full_name": "Updated Name"
        }
    )
    
    assert response.status_code == 200
    data = response.json()
    
    assert data["full_name"] == "Updated Name"
    assert data["email"] == sample_customer.email


def test_update_profile_email(client, sample_customer, auth_headers):
    """Test updating profile email."""
    response = client.put(
        "/api/auth/profile",
        headers=auth_headers,
        json={
            "email": "newemail@example.com"
        }
    )
    
    assert response.status_code == 200
    data = response.json()
    
    assert data["email"] == "newemail@example.com"


def test_update_profile_duplicate_email(client, test_db, sample_customer, auth_headers):
    """Test updating profile with an email already in use."""
    # Create another customer
    other_customer = Customer(
        email="other@example.com",
        password_hash="hash",
        full_name="Other User",
        role="shopper",
        is_active=True
    )
    test_db.add(other_customer)
    test_db.commit()
    
    # Try to update to the other user's email
    response = client.put(
        "/api/auth/profile",
        headers=auth_headers,
        json={
            "email": "other@example.com"
        }
    )
    
    assert response.status_code == 400
    assert "in use" in response.json()["detail"].lower()


def test_update_profile_unauthorized(client):
    """Test updating profile without authentication."""
    response = client.put(
        "/api/auth/profile",
        json={
            "full_name": "Should Fail"
        }
    )
    
    assert response.status_code == 401
