"""Customer domain service: User and address management."""
from typing import Optional
from sqlalchemy.orm import Session
from app.models.customers import User, Address
from app.schemas.customers import (
    UserCreate,
    UserResponse,
    UserListResponse,
    AddressCreate,
    AddressUpdate,
    AddressResponse,
    AddressListResponse,
)


class CustomerService:
    """Service for customer operations."""

    def __init__(self, db: Session):
        self.db = db

    def get_users(
        self,
        page: int = 1,
        page_size: int = 20,
        status: Optional[str] = None,
    ) -> UserListResponse:
        """Get paginated list of users."""
        query = self.db.query(User).filter(User.is_deleted == False)

        if status:
            query = query.filter(User.status == status)

        total = query.count()
        offset = (page - 1) * page_size
        users = query.offset(offset).limit(page_size).all()

        return UserListResponse(
            items=[UserResponse.model_validate(user) for user in users],
            total=total,
            page=page,
            page_size=page_size,
        )

    def get_user_by_id(self, user_id: int) -> Optional[UserResponse]:
        """Get user by ID."""
        user = (
            self.db.query(User)
            .filter(User.id == user_id, User.is_deleted == False)
            .first()
        )
        return UserResponse.model_validate(user) if user else None

    def get_user_by_email(self, email: str) -> Optional[User]:
        """Get user by email (returns ORM model for auth)."""
        return (
            self.db.query(User)
            .filter(User.email == email, User.is_deleted == False)
            .first()
        )

    def create_user(self, data: UserCreate, password_hash: str) -> UserResponse:
        """Create a new user with hashed password."""
        user = User(
            email=data.email,
            name=data.name,
            password_hash=password_hash,
        )
        self.db.add(user)
        self.db.commit()
        self.db.refresh(user)
        return UserResponse.model_validate(user)

    def get_addresses(
        self,
        user_id: int,
        page: int = 1,
        page_size: int = 20,
    ) -> AddressListResponse:
        """Get paginated list of addresses for a user."""
        query = self.db.query(Address).filter(Address.user_id == user_id)

        total = query.count()
        offset = (page - 1) * page_size
        addresses = query.offset(offset).limit(page_size).all()

        return AddressListResponse(
            items=[AddressResponse.model_validate(addr) for addr in addresses],
            total=total,
            page=page,
            page_size=page_size,
        )

    def get_address_by_id(self, address_id: int) -> Optional[AddressResponse]:
        """Get address by ID."""
        address = self.db.query(Address).filter(Address.id == address_id).first()
        return AddressResponse.model_validate(address) if address else None

    def get_default_address(self, user_id: int, address_type: str) -> Optional[AddressResponse]:
        """Get default address for a user."""
        address = (
            self.db.query(Address)
            .filter(
                Address.user_id == user_id,
                Address.address_type == address_type,
                Address.is_default == True,
            )
            .first()
        )
        return AddressResponse.model_validate(address) if address else None

    def create_address(self, data: AddressCreate) -> AddressResponse:
        """Create a new address."""
        # If this is set as default, unset other defaults for this user and type
        if data.is_default:
            self.db.query(Address).filter(
                Address.user_id == data.user_id,
                Address.address_type == data.address_type,
                Address.is_default == True,
            ).update({"is_default": False})

        address = Address(**data.model_dump())
        self.db.add(address)
        self.db.commit()
        self.db.refresh(address)
        return AddressResponse.model_validate(address)

    def update_address(
        self,
        address_id: int,
        data: AddressUpdate,
    ) -> Optional[AddressResponse]:
        """Update an address."""
        address = self.db.query(Address).filter(Address.id == address_id).first()
        if not address:
            return None

        # If setting as default, unset other defaults
        if data.is_default:
            self.db.query(Address).filter(
                Address.user_id == address.user_id,
                Address.address_type == address.address_type,
                Address.is_default == True,
                Address.id != address_id,
            ).update({"is_default": False})

        for key, value in data.model_dump(exclude_unset=True).items():
            setattr(address, key, value)

        self.db.commit()
        self.db.refresh(address)
        return AddressResponse.model_validate(address)

    def delete_address(self, address_id: int) -> bool:
        """Delete an address."""
        address = self.db.query(Address).filter(Address.id == address_id).first()
        if not address:
            return False

        self.db.delete(address)
        self.db.commit()
        return True
