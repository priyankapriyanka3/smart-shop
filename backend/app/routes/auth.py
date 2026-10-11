"""Authentication routes."""
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from pydantic import BaseModel, Field
from app.dependencies import get_db
from app.models.customers import User
from app.auth.jwt import create_access_token
from app.auth.password import verify_password


router = APIRouter()


class LoginRequest(BaseModel):
    """Login request matching shared_config field names."""
    email: str = Field(..., min_length=1)
    password: str = Field(..., min_length=1)


class UserResponse(BaseModel):
    """User data in login response."""
    id: int
    email: str
    name: str
    role: str = "customer"
    
    class Config:
        from_attributes = True


class LoginResponse(BaseModel):
    """Login response matching shared_config structure."""
    access_token: str
    token_type: str = "bearer"
    user: UserResponse


@router.post("/login", response_model=LoginResponse)
def login(
    request: LoginRequest,
    db: Session = Depends(get_db),
):
    """
    Login endpoint with JWT token generation.
    
    Validates credentials using bcrypt password verification and returns JWT token
    with user data. JWT token includes exp claim as required by REQ-AUTH-001.
    
    Rate limited to 5 attempts per email per 15 minutes by RateLimitMiddleware.
    """
    # Find user by email
    user = db.query(User).filter(User.email == request.email).first()
    
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid credentials",
        )
    
    # Verify password using bcrypt directly (not passlib) as required by architecture contract
    if not verify_password(request.password, user.password_hash):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid credentials",
        )
    
    # Check account status
    if user.status != "active":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Account is not active",
        )
    
    # Check soft delete flag (GDPR compliance)
    if user.is_deleted:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Account has been deleted",
        )
    
    # Create access token (JWT with exp claim, embeds str(user.id))
    access_token = create_access_token(user.id)
    
    # Determine user role from user_roles relationship
    user_role = "customer"
    if user.user_roles:
        for ur in user.user_roles:
            if ur.role.name == "admin":
                user_role = "admin"
                break
            elif ur.role.name == "inventory_manager":
                user_role = "inventory_manager"
            elif ur.role.name == "customer_support":
                user_role = "customer_support"
    
    # Return token and user data matching shared_config.auth.login_response structure
    return LoginResponse(
        access_token=access_token,
        user=UserResponse(
            id=user.id,
            email=user.email,
            name=user.name,
            role=user_role,
        ),
    )
