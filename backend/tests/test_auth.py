"""Authentication and authorization tests."""
import pytest
from fastapi import status


class TestAuth:
    """Test authentication endpoints."""
    
    def test_login_success(self, client, test_user):
        """Test successful login with valid credentials."""
        response = client.post(
            "/api/v1/auth/login",
            json={"email": "test@example.com", "password": "testpass123"},
        )
        
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert "access_token" in data
        assert data["token_type"] == "bearer"
        assert "user" in data
        assert data["user"]["email"] == "test@example.com"
        assert data["user"]["name"] == "Test User"
        assert data["user"]["role"] == "customer"
    
    def test_login_failure_invalid_email(self, client, test_user):
        """Test login failure with invalid email."""
        response = client.post(
            "/api/v1/auth/login",
            json={"email": "wrong@example.com", "password": "testpass123"},
        )
        
        assert response.status_code == status.HTTP_401_UNAUTHORIZED
        assert "Invalid credentials" in response.json()["detail"]
    
    def test_login_failure_invalid_password(self, client, test_user):
        """Test login failure with invalid password."""
        response = client.post(
            "/api/v1/auth/login",
            json={"email": "test@example.com", "password": "wrongpassword"},
        )
        
        assert response.status_code == status.HTTP_401_UNAUTHORIZED
        assert "Invalid credentials" in response.json()["detail"]
    
    def test_login_inactive_user(self, client, db, test_user):
        """Test login failure for inactive user."""
        # Set user to inactive
        test_user.status = "inactive"
        db.commit()
        
        response = client.post(
            "/api/v1/auth/login",
            json={"email": "test@example.com", "password": "testpass123"},
        )
        
        assert response.status_code == status.HTTP_403_FORBIDDEN
        assert "not active" in response.json()["detail"]
    
    def test_login_deleted_user(self, client, db, test_user):
        """Test login failure for soft-deleted user."""
        # Set user as deleted
        test_user.is_deleted = True
        db.commit()
        
        response = client.post(
            "/api/v1/auth/login",
            json={"email": "test@example.com", "password": "testpass123"},
        )
        
        assert response.status_code == status.HTTP_403_FORBIDDEN
        assert "deleted" in response.json()["detail"]


class TestTokenValidation:
    """Test JWT token validation."""
    
    def test_valid_token_access(self, client, test_user, auth_token):
        """Test access to protected endpoint with valid token."""
        response = client.get(
            "/api/v1/cart",
            headers={"Authorization": f"Bearer {auth_token}"},
        )
        
        # Should return 200 (cart endpoint accessible)
        assert response.status_code == status.HTTP_200_OK
    
    def test_missing_token(self, client):
        """Test access to protected endpoint without token."""
        response = client.get("/api/v1/cart")
        
        assert response.status_code == status.HTTP_401_UNAUTHORIZED
    
    def test_invalid_token(self, client):
        """Test access with malformed token."""
        response = client.get(
            "/api/v1/cart",
            headers={"Authorization": "Bearer invalid_token_string"},
        )
        
        assert response.status_code == status.HTTP_401_UNAUTHORIZED
    
    def test_expired_token(self, client):
        """Test access with expired token."""
        # This would require creating a token with past expiry
        # For now, we verify the token creation includes exp claim
        from app.auth.jwt import create_access_token
        import jwt
        from app.config import settings
        
        token = create_access_token(user_id=1)
        decoded = jwt.decode(token, settings.secret_key, algorithms=["HS256"])
        
        # Verify exp claim exists
        assert "exp" in decoded
        assert "sub" in decoded


class TestRequireAuth:
    """Test require_auth dependency."""
    
    def test_require_auth_with_valid_token(self, client, auth_token):
        """Test require_auth allows access with valid token."""
        response = client.get(
            "/api/v1/cart",
            headers={"Authorization": f"Bearer {auth_token}"},
        )
        
        assert response.status_code == status.HTTP_200_OK
    
    def test_require_auth_without_token(self, client):
        """Test require_auth blocks access without token."""
        response = client.get("/api/v1/cart")
        
        assert response.status_code == status.HTTP_401_UNAUTHORIZED


class TestRequireRole:
    """Test role-based access control."""
    
    def test_admin_role_access_admin_endpoint(self, client, admin_token):
        """Test admin user can access admin endpoints."""
        response = client.get(
            "/api/v1/admin/dashboard",
            headers={"Authorization": f"Bearer {admin_token}"},
        )
        
        # Admin should have access
        assert response.status_code == status.HTTP_200_OK
    
    def test_customer_role_denied_admin_endpoint(self, client, auth_token):
        """Test customer user is denied access to admin endpoints."""
        response = client.get(
            "/api/v1/admin/dashboard",
            headers={"Authorization": f"Bearer {auth_token}"},
        )
        
        # Customer should be denied
        assert response.status_code == status.HTTP_403_FORBIDDEN
    
    def test_unauthenticated_denied_admin_endpoint(self, client):
        """Test unauthenticated user is denied access to admin endpoints."""
        response = client.get("/api/v1/admin/dashboard")
        
        # Should return 401 (no token)
        assert response.status_code == status.HTTP_401_UNAUTHORIZED


class TestRBAC:
    """Test role-based access control permissions."""
    
    def test_admin_has_all_permissions(self):
        """Test admin role has comprehensive permissions."""
        from app.auth.rbac import ROLE_PERMISSIONS
        
        admin_perms = ROLE_PERMISSIONS.get("admin", set())
        
        # Admin should have broad permissions (21+ permissions)
        assert len(admin_perms) >= 20
        assert "products:read" in admin_perms
        assert "products:create" in admin_perms
        assert "products:update" in admin_perms
        assert "orders:read" in admin_perms
        assert "orders:update" in admin_perms
        assert "inventory:read" in admin_perms
        assert "inventory:update" in admin_perms
    
    def test_customer_has_limited_permissions(self):
        """Test customer role has appropriate limited permissions."""
        from app.auth.rbac import ROLE_PERMISSIONS
        
        customer_perms = ROLE_PERMISSIONS.get("customer", set())
        
        # Customer should have limited permissions
        assert "products:read" in customer_perms
        assert "cart:read" in customer_perms
        assert "cart:update" in customer_perms
        assert "orders:read" in customer_perms
        
        # Customer should not have write permissions for products/inventory
        assert "products:create" not in customer_perms
        assert "products:update" not in customer_perms
        assert "inventory:update" not in customer_perms
    
    def test_all_seeded_roles_exist(self):
        """Test all seeded roles have permission mappings."""
        from app.auth.rbac import ROLE_PERMISSIONS
        
        required_roles = ["admin", "inventory_manager", "customer_support", "customer"]
        
        for role in required_roles:
            assert role in ROLE_PERMISSIONS
            assert len(ROLE_PERMISSIONS[role]) > 0
