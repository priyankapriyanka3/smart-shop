"""
Authentication routes for Smart Shop API.
Handles user registration, login, profile retrieval, and profile updates.
"""
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.auth.dependencies import get_current_user
from app.auth.jwt import create_access_token
from app.auth.password import hash_password, verify_password
from app.database import get_db
from app.models.customer import Customer
from app.schemas.auth import (
    LoginRequest,
    ProfileUpdateRequest,
    RegisterRequest,
    TokenResponse,
    UserResponse,
)

router = APIRouter(prefix="/api/auth", tags=["auth"])


@router.post("/register", response_model=TokenResponse, status_code=status.HTTP_201_CREATED)
def register(
    request: RegisterRequest,
    db: Session = Depends(get_db)
):
    """
    Register a new customer account.
    
    - **email**: Unique email address
    - **password**: Password (min 8 characters)
    - **full_name**: Customer's full name
    
    Returns JWT token and user information.
    """
    # Check if email already exists
    existing_customer = db.query(Customer).filter(Customer.email == request.email).first()
    if existing_customer:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered"
        )
    
    # Validate password complexity (basic check - can be extended)
    if not any(c.isupper() for c in request.password):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Password must contain at least one uppercase letter"
        )
    if not any(c.islower() for c in request.password):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Password must contain at least one lowercase letter"
        )
    if not any(c.isdigit() for c in request.password):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Password must contain at least one number"
        )
    
    # Create new customer
    customer = Customer(
        email=request.email,
        password_hash=hash_password(request.password),
        full_name=request.full_name,
        role="shopper",  # Default role
        is_active=True
    )
    db.add(customer)
    db.commit()
    db.refresh(customer)
    
    # Generate token
    access_token = create_access_token(customer.id, customer.role)
    
    return TokenResponse(
        access_token=access_token,
        user=UserResponse.model_validate(customer)
    )


@router.post("/login", response_model=TokenResponse)
def login(
    request: LoginRequest,
    db: Session = Depends(get_db)
):
    """
    Authenticate and sign in a customer.
    
    - **email**: Customer email
    - **password**: Customer password
    
    Returns JWT token and user information.
    """
    # Find customer by email
    customer = db.query(Customer).filter(Customer.email == request.email).first()
    
    # Generic error message for security (don't reveal if email exists)
    if not customer or not verify_password(request.password, customer.password_hash):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password"
        )
    
    # Check if account is active
    if not customer.is_active:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Account is disabled"
        )
    
    # Generate token
    access_token = create_access_token(customer.id, customer.role)
    
    return TokenResponse(
        access_token=access_token,
        user=UserResponse.model_validate(customer)
    )


@router.get("/me", response_model=UserResponse)
def get_current_user_profile(
    current_user: Customer = Depends(get_current_user)
):
    """
    Get the current authenticated user's profile.
    
    Requires authentication via Bearer token.
    """
    return UserResponse.model_validate(current_user)


@router.put("/profile", response_model=UserResponse)
def update_profile(
    request: ProfileUpdateRequest,
    current_user: Customer = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Update the current user's profile.
    
    - **full_name**: New full name (optional)
    - **email**: New email address (optional)
    
    Requires authentication via Bearer token.
    """
    # Update full name if provided
    if request.full_name is not None:
        current_user.full_name = request.full_name
    
    # Update email if provided
    if request.email is not None:
        # Check if new email is already taken by another user
        existing = db.query(Customer).filter(
            Customer.email == request.email,
            Customer.id != current_user.id
        ).first()
        if existing:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Email already in use"
            )
        current_user.email = request.email
    
    db.commit()
    db.refresh(current_user)
    
    return UserResponse.model_validate(current_user)
