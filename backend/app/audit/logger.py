"""Audit logging helper functions for operational changes."""
from typing import Optional, List
from datetime import datetime
from sqlalchemy.orm import Session
from app.models.audit import AuditLog


def log_audit(
    db: Session,
    user_id: int,
    object_type: str,
    object_id: int,
    action: str,
    summary: Optional[str] = None,
) -> AuditLog:
    """
    Create an audit log entry for an operational change.
    
    Args:
        db: Database session
        user_id: ID of the user performing the action
        object_type: Type of object being modified (order, promotion, review, inventory, etc.)
        object_id: ID of the object being modified
        action: Action performed (create, update, delete, approve, reject, adjust, etc.)
        summary: Optional detailed summary of the change
    
    Returns:
        Created AuditLog record
    
    Example:
        log_audit(
            db=db,
            user_id=current_user.id,
            object_type="order",
            object_id=order.id,
            action="status_update",
            summary=f"Order status changed from {old_status} to {new_status}"
        )
    """
    audit_entry = AuditLog(
        user_id=user_id,
        object_type=object_type,
        object_id=object_id,
        action=action,
        summary=summary,
        created_at=datetime.utcnow(),
    )
    
    db.add(audit_entry)
    db.commit()
    db.refresh(audit_entry)
    
    return audit_entry


def get_audit_logs(
    db: Session,
    object_type: Optional[str] = None,
    object_id: Optional[int] = None,
    user_id: Optional[int] = None,
    action: Optional[str] = None,
    limit: int = 100,
    offset: int = 0,
) -> List[AuditLog]:
    """
    Retrieve audit log entries with optional filtering.
    
    Args:
        db: Database session
        object_type: Filter by object type
        object_id: Filter by object ID
        user_id: Filter by user who performed the action
        action: Filter by action type
        limit: Maximum number of records to return
        offset: Number of records to skip
    
    Returns:
        List of AuditLog records matching the filters
    """
    query = db.query(AuditLog)
    
    if object_type:
        query = query.filter(AuditLog.object_type == object_type)
    
    if object_id is not None:
        query = query.filter(AuditLog.object_id == object_id)
    
    if user_id is not None:
        query = query.filter(AuditLog.user_id == user_id)
    
    if action:
        query = query.filter(AuditLog.action == action)
    
    query = query.order_by(AuditLog.created_at.desc())
    query = query.limit(limit).offset(offset)
    
    return query.all()
