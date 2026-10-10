"""AuditLog model for tracking privileged actions."""
from __future__ import annotations

from datetime import datetime

from sqlalchemy import Column, DateTime, ForeignKey, Index, Integer, String, Text
from sqlalchemy.orm import relationship

from app.database import Base


class AuditLog(Base):
    """Audit log for privileged actions."""

    __tablename__ = "audit_log"

    id = Column(Integer, primary_key=True, index=True)
    actor_id = Column(Integer, ForeignKey("customer.id"), nullable=False)
    action = Column(String(128), nullable=False)
    entity_type = Column(String(64), nullable=False)
    entity_id = Column(String(64), nullable=False)
    details = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)

    # Relationships
    actor = relationship("Customer", back_populates="audit_logs")

    # Indexes
    __table_args__ = (
        Index("idx_audit_entity_created", "entity_type", "entity_id", "created_at"),
    )
