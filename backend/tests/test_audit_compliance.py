"""Tests for audit logging and GDPR compliance controls."""
import pytest
from datetime import datetime
from sqlalchemy.orm import Session
from app.models.audit import AuditLog
from app.models.customers import User, Address
from app.models.orders import Order
from app.models.promotions import Promotion
from app.models.reviews import Review
from app.models.inventory import Inventory
from app.audit.logger import log_audit, get_audit_logs
from app.privacy.gdpr import (
    mask_email,
    mask_name,
    mask_pii,
    get_pii_fields,
    soft_delete_user,
    anonymize_user_data,
)


class TestAuditLogging:
    """Test audit logging functionality."""

    def test_audit_logs_table_structure(self, db: Session):
        """Verify audit_logs table includes required columns."""
        # Create a test audit log entry
        log_entry = log_audit(
            db=db,
            user_id=1,
            object_type="order",
            object_id=1,
            action="status_update",
            summary="Test audit entry",
        )
        
        # Verify all required columns exist
        assert hasattr(log_entry, "id")
        assert hasattr(log_entry, "user_id")
        assert hasattr(log_entry, "timestamp") or hasattr(log_entry, "created_at")
        assert hasattr(log_entry, "object_type")
        assert hasattr(log_entry, "object_id")
        assert hasattr(log_entry, "action")
        assert hasattr(log_entry, "summary")
        
        # Verify values
        assert log_entry.user_id == 1
        assert log_entry.object_type == "order"
        assert log_entry.object_id == 1
        assert log_entry.action == "status_update"
        assert log_entry.summary == "Test audit entry"

    def test_log_audit_helper_function(self, db: Session, test_user: User):
        """Verify audit logging helper creates entries correctly."""
        # Log an audit entry
        entry = log_audit(
            db=db,
            user_id=test_user.id,
            object_type="promotion",
            object_id=42,
            action="activate",
            summary="Promotion activated by admin",
        )
        
        # Verify entry was created
        assert entry.id is not None
        assert entry.user_id == test_user.id
        assert entry.object_type == "promotion"
        assert entry.object_id == 42
        assert entry.action == "activate"

    def test_order_status_update_logs_audit_entry(
        self, db: Session, test_user: User, test_order: Order
    ):
        """Verify order status update logs audit entry with acting user."""
        from app.services.orders import OrderService
        
        service = OrderService(db)
        service.update_order_status(
            order_id=test_order.id,
            status="shipped",
            user_id=test_user.id,
        )
        
        # Check audit log was created
        logs = get_audit_logs(db, object_type="order", object_id=test_order.id)
        assert len(logs) > 0
        assert logs[0].action == "status_update"
        assert logs[0].user_id == test_user.id

    def test_promotion_activate_logs_audit_entry(
        self, db: Session, test_user: User, test_promotion: Promotion
    ):
        """Verify promotion activate/deactivate logs audit entry."""
        from app.services.promotions import PromotionService
        
        service = PromotionService(db)
        
        # Activate promotion
        service.activate_promotion(test_promotion.id, user_id=test_user.id)
        
        # Check audit log
        logs = get_audit_logs(db, object_type="promotion", object_id=test_promotion.id, action="activate")
        assert len(logs) > 0
        assert logs[0].user_id == test_user.id
        
        # Deactivate promotion
        service.deactivate_promotion(test_promotion.id, user_id=test_user.id)
        
        # Check audit log
        logs = get_audit_logs(db, object_type="promotion", object_id=test_promotion.id, action="deactivate")
        assert len(logs) > 0
        assert logs[0].user_id == test_user.id

    def test_review_approve_reject_logs_audit_entry(
        self, db: Session, test_user: User, test_review: Review
    ):
        """Verify review approve/reject logs audit entry."""
        from app.services.reviews import ReviewService
        
        service = ReviewService(db)
        
        # Approve review
        service.approve_review(test_review.id, user_id=test_user.id)
        
        # Check audit log
        logs = get_audit_logs(db, object_type="review", object_id=test_review.id, action="approve")
        assert len(logs) > 0
        assert logs[0].user_id == test_user.id

    def test_inventory_adjustment_logs_audit_entry(
        self, db: Session, test_user: User, test_inventory: Inventory
    ):
        """Verify inventory adjustment logs audit entry with reason."""
        from app.services.inventory import InventoryService
        
        service = InventoryService(db)
        service.adjust_stock(
            inventory_id=test_inventory.id,
            quantity_change=10,
            reason="Received shipment from supplier",
            user_id=test_user.id,
        )
        
        # Check audit log
        logs = get_audit_logs(db, object_type="inventory", object_id=test_inventory.id)
        assert len(logs) > 0
        assert logs[0].action == "adjust"
        assert logs[0].user_id == test_user.id
        assert "Received shipment" in logs[0].summary


class TestGDPRCompliance:
    """Test GDPR data privacy controls."""

    def test_pii_fields_documented(self):
        """Verify PII fields are documented."""
        pii_fields = get_pii_fields()
        
        # Check user PII fields
        assert "user" in pii_fields
        assert "email" in pii_fields["user"]
        assert "name" in pii_fields["user"]
        
        # Check address PII fields
        assert "address" in pii_fields
        assert "street" in pii_fields["address"]
        assert "city" in pii_fields["address"]

    def test_mask_email(self):
        """Verify email masking for logs."""
        masked = mask_email("john.doe@example.com")
        assert masked == "j***@example.com"
        assert "john.doe" not in masked

    def test_mask_name(self):
        """Verify name masking for logs."""
        masked = mask_name("John Doe")
        assert masked == "J*** D***"
        assert "John" not in masked
        assert "Doe" not in masked

    def test_mask_pii_in_logs(self):
        """Verify logs mask PII (no email/name in log output)."""
        data = {
            "email": "user@example.com",
            "name": "Test User",
            "order_id": 123,
            "total": 99.99,
        }
        
        masked = mask_pii(data)
        
        # Verify PII is masked
        assert "user@example.com" not in str(masked["email"])
        assert "Test User" not in str(masked["name"])
        assert masked["email"] == "u***@example.com"
        
        # Verify non-PII is unchanged
        assert masked["order_id"] == 123
        assert masked["total"] == 99.99

    def test_user_model_has_is_deleted_flag(self, db: Session):
        """Verify User model has is_deleted boolean flag for soft delete."""
        user = User(
            email="test@example.com",
            name="Test User",
            password_hash="hashed",
            status="active",
            is_deleted=False,
        )
        db.add(user)
        db.commit()
        
        assert hasattr(user, "is_deleted")
        assert isinstance(user.is_deleted, bool)
        assert user.is_deleted is False

    def test_user_consent_tracking(self, db: Session):
        """Verify consent tracking: user.consent_timestamp field."""
        user = User(
            email="consent@example.com",
            name="Consent User",
            password_hash="hashed",
            status="active",
            consent_timestamp=datetime.utcnow(),
        )
        db.add(user)
        db.commit()
        
        assert hasattr(user, "consent_timestamp")
        assert user.consent_timestamp is not None
        assert isinstance(user.consent_timestamp, datetime)

    def test_soft_delete_user(self, db: Session, test_user: User, admin_user: User):
        """Verify soft delete functionality."""
        # Soft delete user
        result = soft_delete_user(db, test_user.id, actor_user_id=admin_user.id)
        
        # Verify user is marked as deleted
        assert result.is_deleted is True
        assert result.status == "inactive"
        
        # Verify audit log was created
        logs = get_audit_logs(db, object_type="user", object_id=test_user.id, action="soft_delete")
        assert len(logs) > 0

    def test_anonymize_user_data(self, db: Session, test_user_with_address: User, admin_user: User):
        """Verify data anonymization for GDPR compliance."""
        original_email = test_user_with_address.email
        
        # Anonymize user
        result = anonymize_user_data(
            db,
            test_user_with_address.id,
            actor_user_id=admin_user.id,
        )
        
        # Verify PII is anonymized
        assert result.email != original_email
        assert "deleted_user" in result.email
        assert result.name.startswith("Deleted User")
        assert result.password_hash == "ANONYMIZED"
        assert result.is_deleted is True
        
        # Verify audit log
        logs = get_audit_logs(db, object_type="user", object_id=test_user_with_address.id, action="anonymize")
        assert len(logs) > 0


class TestAuditQueryability:
    """Test audit log querying."""

    def test_query_audit_logs_after_order_update(
        self, db: Session, test_user: User, test_order: Order
    ):
        """Query audit_logs table after order update shows entry."""
        from app.services.orders import OrderService
        
        service = OrderService(db)
        service.update_order_status(test_order.id, "delivered", user_id=test_user.id)
        
        # Query audit logs
        result = db.query(AuditLog).filter(
            AuditLog.object_type == "order",
            AuditLog.object_id == test_order.id,
        ).all()
        
        assert len(result) > 0
        assert result[0].action == "status_update"
        assert result[0].user_id == test_user.id
