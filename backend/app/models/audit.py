"""Audit domain models: Operational audit logs."""
from datetime import datetime
from sqlalchemy import Column, Integer, String, Text, ForeignKey, DateTime, Index
from sqlalchemy.orm import relationship
from app.database import Base


class AuditLog(Base):
    """Immutable audit log for operational changes."""
    __tablename__ = "audit_logs"
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    object_type = Column(String(100), nullable=False)  # order, product, promotion, review, inventory, etc.
    object_id = Column(Integer, nullable=False)
    action = Column(String(100), nullable=False)  # create, update, delete, approve, reject, adjust, etc.
    summary = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)
    
    # Relationships
    user = relationship("User", back_populates="audit_logs", foreign_keys=[user_id])


# Indexes for performance
Index("idx_audit_user", AuditLog.user_id)
Index("idx_audit_object", AuditLog.object_type, AuditLog.object_id)
Index("idx_audit_action", AuditLog.action)
Index("idx_audit_created", AuditLog.created_at)
