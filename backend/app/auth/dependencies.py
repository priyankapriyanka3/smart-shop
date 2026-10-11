"""
FastAPI authentication dependencies.
"""

from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from sqlalchemy.orm import Session

from app.auth.jwt import decode_access_token
from app.database import get_db
from app.models.customer import Customer

security = HTTPBearer()


def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: Session = Depends(get_db)
) -> Customer:
    """
    Get the current authenticated user from JWT token.

    Args:
        credentials: Bearer token from Authorization header
        db: Database session

    Returns:
        Authenticated Customer model

    Raises:
        HTTPException: 401 if token is invalid or user not found
    """
    token = credentials.credentials
    payload = decode_access_token(token)

    if payload is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials"
        )

    customer_id = int(payload.get("sub"))
    customer = db.query(Customer).filter(Customer.id == customer_id).first()

    if customer is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User not found"
        )

    return customer


def require_role(*allowed_roles: str):
    """
    Create a dependency that requires specific roles.

    Args:
        *allowed_roles: Role names that are allowed (e.g., "admin", "inventory_manager")

    Returns:
        Dependency function that checks user role
    """
    def check_role(current_user: Customer = Depends(get_current_user)) -> Customer:
        if current_user.role not in allowed_roles:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f"Insufficient permissions. Required roles: {', '.join(allowed_roles)}"
            )
        return current_user

    return check_role


# Common role dependencies
require_admin = require_role("admin")
require_inventory_manager = require_role("inventory_manager")
require_customer_support = require_role("customer_support")
require_staff = require_role("admin", "inventory_manager", "customer_support")
