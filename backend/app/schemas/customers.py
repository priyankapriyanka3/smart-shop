"""Customer domain schemas: Users and Addresses."""
from datetime import datetime
from typing import Optional, List
from pydantic import BaseModel, EmailStr, Field, ConfigDict


class UserBase(BaseModel):
    """Base user schema."""
    email: EmailStr
    name: str = Field(..., min_length=1, max_length=255)


class UserCreate(UserBase):
    """User creation request."""
    password: str = Field(..., min_length=8, max_length=255)


class UserResponse(UserBase):
    """User response."""
    id: int
    status: str
    consent_timestamp: Optional[datetime] = None
    created_at: datetime
    updated_at: datetime
    
    model_config = ConfigDict(from_attributes=True)


class UserListResponse(BaseModel):
    """Paginated user list response."""
    items: List[UserResponse]
    total: int
    page: int
    page_size: int


class AddressBase(BaseModel):
    """Base address schema."""
    address_type: str = Field(..., pattern="^(shipping|billing)$")
    street: str = Field(..., min_length=1, max_length=500)
    city: str = Field(..., min_length=1, max_length=255)
    state_province: str = Field(..., min_length=1, max_length=255)
    postal_code: str = Field(..., min_length=1, max_length=50)
    country: str = Field(..., min_length=1, max_length=100)
    is_default: bool = False


class AddressCreate(AddressBase):
    """Address creation request."""
    user_id: int = Field(..., gt=0)


class AddressUpdate(BaseModel):
    """Address update request."""
    street: Optional[str] = Field(None, min_length=1, max_length=500)
    city: Optional[str] = Field(None, min_length=1, max_length=255)
    state_province: Optional[str] = Field(None, min_length=1, max_length=255)
    postal_code: Optional[str] = Field(None, min_length=1, max_length=50)
    country: Optional[str] = Field(None, min_length=1, max_length=100)
    is_default: Optional[bool] = None


class AddressResponse(AddressBase):
    """Address response."""
    id: int
    user_id: int
    created_at: datetime
    updated_at: datetime
    
    model_config = ConfigDict(from_attributes=True)


class AddressListResponse(BaseModel):
    """Paginated address list response."""
    items: List[AddressResponse]
    total: int
    page: int
    page_size: int
