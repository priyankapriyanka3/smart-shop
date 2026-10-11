"""GDPR data privacy controls and PII masking utilities."""
from typing import Dict, List, Optional, Any
from datetime import datetime
from sqlalchemy.orm import Session
from app.models.customers import User, Address


# Document PII fields across the system
PII_FIELDS = {
    "user": ["email", "name"],
    "address": ["street", "city", "state_province", "postal_code"],
}


def get_pii_fields() -> Dict[str, List[str]]:
    """
    Get documented PII fields across all tables.
    
    Returns:
        Dictionary mapping table/model names to list of PII field names
    """
    return PII_FIELDS.copy()


def mask_email(email: str) -> str:
    """
    Mask email address for logging and display.
    
    Example: john.doe@example.com -> j***@example.com
    
    Args:
        email: Email address to mask
    
    Returns:
        Masked email string
    """
    if not email or "@" not in email:
        return "***"
    
    local, domain = email.split("@", 1)
    if len(local) <= 1:
        return f"*@{domain}"
    
    return f"{local[0]}***@{domain}"


def mask_name(name: str) -> str:
    """
    Mask person's name for logging and display.
    
    Example: John Doe -> J*** D***
    
    Args:
        name: Full name to mask
    
    Returns:
        Masked name string
    """
    if not name:
        return "***"
    
    parts = name.strip().split()
    masked_parts = []
    
    for part in parts:
        if len(part) == 0:
            continue
        elif len(part) == 1:
            masked_parts.append("*")
        else:
            masked_parts.append(f"{part[0]}***")
    
    return " ".join(masked_parts) if masked_parts else "***"


def mask_pii(data: Dict[str, Any], field_names: Optional[List[str]] = None) -> Dict[str, Any]:
    """
    Mask PII fields in a dictionary for safe logging.
    
    Args:
        data: Dictionary containing data that may include PII
        field_names: Optional list of field names to mask. If None, uses default PII field list.
    
    Returns:
        Dictionary with PII fields masked
    """
    if field_names is None:
        # Default PII fields to mask
        field_names = ["email", "name", "street", "city", "password", "password_hash"]
    
    masked_data = data.copy()
    
    for field in field_names:
        if field in masked_data:
            value = masked_data[field]
            
            if field == "email" and isinstance(value, str):
                masked_data[field] = mask_email(value)
            elif field == "name" and isinstance(value, str):
                masked_data[field] = mask_name(value)
            elif field in ["password", "password_hash"]:
                masked_data[field] = "***"
            elif isinstance(value, str):
                # Generic masking for other string fields
                if len(value) <= 2:
                    masked_data[field] = "***"
                else:
                    masked_data[field] = f"{value[:2]}***"
    
    return masked_data


def soft_delete_user(db: Session, user_id: int, actor_user_id: int) -> User:
    """
    Soft delete a user account for GDPR right to erasure.
    
    Sets is_deleted flag to True and marks the account as inactive.
    Does not remove the record from the database to maintain referential integrity
    for orders, reviews, and audit logs.
    
    Args:
        db: Database session
        user_id: ID of user to soft delete
        actor_user_id: ID of user performing the deletion (for audit)
    
    Returns:
        Updated User record
    
    Raises:
        ValueError: If user not found or already deleted
    """
    from app.audit.logger import log_audit
    
    user = db.query(User).filter(User.id == user_id).first()
    
    if not user:
        raise ValueError(f"User {user_id} not found")
    
    if user.is_deleted:
        raise ValueError(f"User {user_id} is already deleted")
    
    # Mark as deleted and inactive
    user.is_deleted = True
    user.status = "inactive"
    user.updated_at = datetime.utcnow()
    
    db.commit()
    db.refresh(user)
    
    # Log the deletion action
    log_audit(
        db=db,
        user_id=actor_user_id,
        object_type="user",
        object_id=user_id,
        action="soft_delete",
        summary=f"User account soft deleted for GDPR compliance",
    )
    
    return user


def anonymize_user_data(db: Session, user_id: int, actor_user_id: int) -> User:
    """
    Anonymize user personal data for GDPR right to erasure.
    
    Replaces PII fields with anonymized values while maintaining referential integrity.
    This is a more aggressive approach than soft delete and is typically used when
    the user explicitly requests data erasure.
    
    Args:
        db: Database session
        user_id: ID of user to anonymize
        actor_user_id: ID of user performing the anonymization (for audit)
    
    Returns:
        Anonymized User record
    
    Raises:
        ValueError: If user not found
    """
    from app.audit.logger import log_audit
    
    user = db.query(User).filter(User.id == user_id).first()
    
    if not user:
        raise ValueError(f"User {user_id} not found")
    
    # Anonymize PII fields
    user.email = f"deleted_user_{user_id}@anonymized.local"
    user.name = f"Deleted User {user_id}"
    user.password_hash = "ANONYMIZED"
    user.is_deleted = True
    user.status = "inactive"
    user.consent_timestamp = None
    user.updated_at = datetime.utcnow()
    
    # Anonymize associated addresses
    addresses = db.query(Address).filter(Address.user_id == user_id).all()
    for address in addresses:
        address.street = "ANONYMIZED"
        address.city = "ANONYMIZED"
        address.state_province = "ANONYMIZED"
        address.postal_code = "00000"
    
    db.commit()
    db.refresh(user)
    
    # Log the anonymization action
    log_audit(
        db=db,
        user_id=actor_user_id,
        object_type="user",
        object_id=user_id,
        action="anonymize",
        summary=f"User personal data anonymized for GDPR compliance",
    )
    
    return user
