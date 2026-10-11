"""FastAPI dependencies for authentication and authorization."""
from typing import Optional, Callable
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.orm import Session
from app.dependencies import get_db
from app.auth.jwt import decode_access_token
from app.models.customers import User
from app.auth.rbac import check_permission


# HTTP Bearer token scheme for Authorization header
security = HTTPBearer()


def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: Session = Depends(get_db),
) -> User:
    """
    Extract and validate current user from JWT token.
    
    Dependency for protected routes that require authentication.
    Returns User object if token is valid.
    
    Args:
        credentials: HTTP Bearer token from Authorization header
        db: Database session
    
    Returns:
        User object
    
    Raises:
        HTTPException 401: If token is invalid or user not found
    """
    token = credentials.credentials
    
    # Decode JWT token
    payload = decode_access_token(token)
    if payload is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired token",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    # Extract user_id from token payload (stored as string)
    user_id_str: Optional[str] = payload.get("sub")
    if user_id_str is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token payload",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    try:
        user_id = int(user_id_str)
    except ValueError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token payload",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    # Load user from database
    user = db.query(User).filter(User.id == user_id).first()
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User not found",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    # Check account status
    if user.status != "active":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Account is not active",
        )
    
    # Check soft delete flag
    if user.is_deleted:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Account has been deleted",
        )
    
    return user


def require_auth(user: User = Depends(get_current_user)) -> User:
    """
    Require authentication dependency.
    
    Returns 401 if no valid token provided.
    Alias for get_current_user for clearer semantic intent.
    
    Args:
        user: Current user from get_current_user dependency
    
    Returns:
        User object
    """
    return user


def require_role(role_name: str) -> Callable:
    """
    Create dependency that requires specific role.
    
    Returns 403 if user lacks the required role.
    
    Args:
        role_name: Required role name (e.g., "admin", "inventory_manager")
    
    Returns:
        Dependency function
    
    Example:
        @router.get("/admin/dashboard", dependencies=[Depends(require_role("admin"))])
        def admin_dashboard():
            ...
    """
    def role_checker(user: User = Depends(get_current_user)) -> User:
        # Check if user has the required role
        user_roles = [ur.role.name for ur in user.user_roles]
        
        if role_name not in user_roles:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f"Role '{role_name}' required",
            )
        
        return user
    
    return role_checker


def require_permission(resource: str, action: str) -> Callable:
    """
    Create dependency that requires specific permission.
    
    Returns 403 if user lacks the required permission.
    
    Args:
        resource: Resource name (e.g., "products", "orders")
        action: Action name (e.g., "read", "create", "update", "delete")
    
    Returns:
        Dependency function
    
    Example:
        @router.post("/products", dependencies=[Depends(require_permission("products", "create"))])
        def create_product():
            ...
    """
    def permission_checker(user: User = Depends(get_current_user)) -> User:
        # Get user roles
        user_roles = [ur.role.name for ur in user.user_roles]
        
        # Check if any role has the required permission
        has_permission = any(
            check_permission(role_name, resource, action)
            for role_name in user_roles
        )
        
        if not has_permission:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f"Permission '{resource}:{action}' required",
            )
        
        return user
    
    return permission_checker
