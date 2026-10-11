"""Admin domain models: Roles, Permissions, and User-Role assignments."""
from datetime import datetime
from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, Index
from sqlalchemy.orm import relationship
from app.database import Base


class Role(Base):
    """User role for RBAC."""
    __tablename__ = "roles"
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(100), nullable=False, unique=True, index=True)
    description = Column(String(500), nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)
    
    # Relationships
    user_roles = relationship("UserRole", back_populates="role")
    permissions = relationship("Permission", back_populates="role")


class Permission(Base):
    """Permission assigned to a role."""
    __tablename__ = "permissions"
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    role_id = Column(Integer, ForeignKey("roles.id"), nullable=False)
    resource = Column(String(100), nullable=False)  # products, orders, inventory, promotions, reviews, etc.
    action = Column(String(100), nullable=False)  # create, read, update, delete, approve, etc.
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)
    
    # Relationships
    role = relationship("Role", back_populates="permissions")


class UserRole(Base):
    """User-to-Role assignment for RBAC."""
    __tablename__ = "user_roles"
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    role_id = Column(Integer, ForeignKey("roles.id"), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)
    
    # Relationships
    user = relationship("User", back_populates="user_roles")
    role = relationship("Role", back_populates="user_roles")


# Indexes for performance
Index("idx_permission_role", Permission.role_id)
Index("idx_user_role_user", UserRole.user_id)
Index("idx_user_role_role", UserRole.role_id)
# Unique constraint to prevent duplicate role assignments
Index("idx_user_role_unique", UserRole.user_id, UserRole.role_id, unique=True)
