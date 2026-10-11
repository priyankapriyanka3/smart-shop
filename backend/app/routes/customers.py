"""Customer routes: profile and address management."""
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.dependencies import get_db
from app.services.customers import CustomerService
from app.schemas.customers import (
    UserCreate,
    UserResponse,
    AddressCreate,
    AddressResponse,
    AddressListResponse,
)


router = APIRouter()


@router.post("/register", response_model=UserResponse, status_code=201)
def register_user(
    data: UserCreate,
    db: Session = Depends(get_db),
):
    """
    Register a new customer account.
    
    Enforces email uniqueness and creates account with active status.
    """
    import bcrypt
    
    service = CustomerService(db)
    # Hash the password before creating user
    password_hash = bcrypt.hashpw(data.password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
    return service.create_user(data, password_hash)


@router.get("/profile/{user_id}", response_model=UserResponse)
def get_profile(
    user_id: int,
    db: Session = Depends(get_db),
):
    """Get customer profile by ID."""
    service = CustomerService(db)
    user = service.get_user_by_id(user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user


@router.get("/addresses/{user_id}", response_model=AddressListResponse)
def list_addresses(
    user_id: int,
    db: Session = Depends(get_db),
):
    """Get all addresses for a user."""
    service = CustomerService(db)
    return service.get_addresses(user_id)


@router.post("/addresses", response_model=AddressResponse, status_code=201)
def create_address(
    data: AddressCreate,
    db: Session = Depends(get_db),
):
    """Create a new address for a user."""
    service = CustomerService(db)
    return service.create_address(data)


@router.get("/addresses/detail/{address_id}", response_model=AddressResponse)
def get_address(
    address_id: int,
    db: Session = Depends(get_db),
):
    """Get address by ID."""
    service = CustomerService(db)
    address = service.get_address_by_id(address_id)
    if not address:
        raise HTTPException(status_code=404, detail="Address not found")
    return address
