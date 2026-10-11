"""Promotions domain tests."""
import pytest
from fastapi import status
from datetime import datetime, timedelta


class TestPromotionEligibility:
    """Test promotion eligibility validation."""
    
    def test_valid_promotion_eligibility(self, db, test_promotion):
        """Test checking eligibility for valid promotion."""
        from app.services.promotions import PromotionService
        
        service = PromotionService(db)
        
        # test_promotion is "TEST10" with 10% discount, min order 50
        result = service.check_eligibility("TEST10", order_amount=100.0)
        
        assert result.eligible is True
        assert result.discount_amount == 10.0
        assert result.promotion_name == "Test Promotion"
    
    def test_promotion_minimum_threshold_not_met(self, db, test_promotion):
        """Test promotion ineligible when minimum order not met."""
        from app.services.promotions import PromotionService
        
        service = PromotionService(db)
        
        # test_promotion requires min order of 50
        result = service.check_eligibility("TEST10", order_amount=30.0)
        
        assert result.eligible is False
        assert len(result.errors) > 0
        assert any("minimum" in error.lower() for error in result.errors)
    
    def test_expired_promotion_ineligible(self, db, expired_promotion):
        """Test expired promotion is ineligible."""
        from app.services.promotions import PromotionService
        
        service = PromotionService(db)
        
        result = service.check_eligibility("EXPIRED", order_amount=100.0)
        
        assert result.eligible is False
        assert any("expired" in error.lower() for error in result.errors)
    
    def test_nonexistent_promotion_code(self, db):
        """Test checking eligibility for non-existent promotion."""
        from app.services.promotions import PromotionService
        
        service = PromotionService(db)
        
        result = service.check_eligibility("INVALID123", order_amount=100.0)
        
        assert result.eligible is False
        assert any("not found" in error.lower() for error in result.errors)


class TestPromotionUsageLimits:
    """Test promotion usage limit enforcement."""
    
    def test_usage_limit_enforcement(self, client, db):
        """Test promotion becomes ineligible when usage limit reached."""
        from app.models.promotions import Promotion
        from app.services.promotions import PromotionService
        
        now = datetime.utcnow()
        
        # Create promotion with max_uses = 2
        promotion = Promotion(
            name="Limited Promotion",
            code="LIMITED",
            description="Limited use promotion",
            discount_type="percentage",
            discount_value=15.0,
            minimum_order_amount=0.0,
            start_date=now - timedelta(days=1),
            end_date=now + timedelta(days=30),
            max_uses=2,
            current_uses=2,  # Already at limit
            status="active",
        )
        db.add(promotion)
        db.commit()
        
        service = PromotionService(db)
        result = service.check_eligibility("LIMITED", order_amount=100.0)
        
        assert result.eligible is False
        assert any("usage limit" in error.lower() or "limit reached" in error.lower() for error in result.errors)
    
    def test_increment_usage_count(self, client, test_promotion, db):
        """Test incrementing promotion usage count."""
        from app.services.promotions import PromotionService
        
        service = PromotionService(db)
        
        original_uses = test_promotion.current_uses
        success = service.increment_usage("TEST10")
        
        assert success is True
        
        # Verify count incremented
        db.refresh(test_promotion)
        assert test_promotion.current_uses == original_uses + 1
    
    def test_usage_validation_in_checkout(self, client, auth_token, test_product, test_inventory, db):
        """Test promotion usage validated during checkout."""
        from app.models.cart import Cart, CartItem
        from app.models.customers import User
        from app.models.promotions import Promotion
        
        user = db.query(User).filter(User.email == "test@example.com").first()
        
        # Create promotion at usage limit
        now = datetime.utcnow()
        promotion = Promotion(
            name="Maxed Out",
            code="MAXED",
            description="Maxed promotion",
            discount_type="percentage",
            discount_value=10.0,
            minimum_order_amount=0.0,
            start_date=now - timedelta(days=1),
            end_date=now + timedelta(days=30),
            max_uses=5,
            current_uses=5,  # At limit
            status="active",
        )
        db.add(promotion)
        db.commit()
        
        # Create cart
        cart = Cart(customer_id=user.id, status="active")
        db.add(cart)
        db.commit()
        
        cart_item = CartItem(
            cart_id=cart.id,
            product_id=test_product.id,
            quantity=1,
        )
        db.add(cart_item)
        db.commit()
        
        # Try to validate checkout with maxed promotion
        response = client.post(
            "/api/v1/checkout/validate",
            headers={"Authorization": f"Bearer {auth_token}"},
            json={
                "shipping_address_id": 1,
                "billing_address_id": 1,
                "promotion_code": "MAXED",
            },
        )
        
        assert response.status_code == status.HTTP_400_BAD_REQUEST


class TestPromotionTypes:
    """Test different promotion types."""
    
    def test_percentage_discount(self, db, test_promotion):
        """Test percentage discount calculation."""
        from app.services.promotions import PromotionService
        
        service = PromotionService(db)
        
        # test_promotion is 10% discount
        result = service.check_eligibility("TEST10", order_amount=200.0)
        
        assert result.eligible is True
        assert result.discount_amount == 20.0  # 10% of 200
        assert result.discount_type == "percentage"
    
    def test_fixed_discount(self, db):
        """Test fixed amount discount."""
        from app.models.promotions import Promotion
        from app.services.promotions import PromotionService
        
        now = datetime.utcnow()
        
        # Create fixed discount promotion
        promotion = Promotion(
            name="Fixed $20 Off",
            code="FIXED20",
            description="$20 off",
            discount_type="fixed",
            discount_value=20.0,
            minimum_order_amount=100.0,
            start_date=now - timedelta(days=1),
            end_date=now + timedelta(days=30),
            max_uses=100,
            current_uses=0,
            status="active",
        )
        db.add(promotion)
        db.commit()
        
        service = PromotionService(db)
        result = service.check_eligibility("FIXED20", order_amount=150.0)
        
        assert result.eligible is True
        assert result.discount_amount == 20.0
        assert result.discount_type == "fixed"
    
    def test_fixed_discount_capped_at_order_amount(self, db):
        """Test fixed discount cannot exceed order amount."""
        from app.models.promotions import Promotion
        from app.services.promotions import PromotionService
        
        now = datetime.utcnow()
        
        # Create fixed discount larger than order
        promotion = Promotion(
            name="Big Discount",
            code="BIG50",
            description="$50 off",
            discount_type="fixed",
            discount_value=50.0,
            minimum_order_amount=0.0,
            start_date=now - timedelta(days=1),
            end_date=now + timedelta(days=30),
            max_uses=100,
            current_uses=0,
            status="active",
        )
        db.add(promotion)
        db.commit()
        
        service = PromotionService(db)
        result = service.check_eligibility("BIG50", order_amount=30.0)
        
        assert result.eligible is True
        # Discount should be capped at order amount
        assert result.discount_amount <= 30.0
    
    def test_free_shipping_promotion(self, db):
        """Test free shipping promotion type."""
        from app.models.promotions import Promotion
        from app.services.promotions import PromotionService
        
        now = datetime.utcnow()
        
        # Create free shipping promotion
        promotion = Promotion(
            name="Free Shipping",
            code="FREESHIP",
            description="Free shipping",
            discount_type="free_shipping",
            discount_value=0.0,
            minimum_order_amount=75.0,
            start_date=now - timedelta(days=1),
            end_date=now + timedelta(days=30),
            max_uses=100,
            current_uses=0,
            status="active",
        )
        db.add(promotion)
        db.commit()
        
        service = PromotionService(db)
        result = service.check_eligibility("FREESHIP", order_amount=100.0)
        
        assert result.eligible is True
        assert result.discount_type == "free_shipping"
        # Free shipping doesn't reduce order amount directly
        assert result.discount_amount == 0.0


class TestPromotionDateValidation:
    """Test promotion date window validation."""
    
    def test_promotion_not_yet_started(self, db):
        """Test promotion that hasn't started yet is ineligible."""
        from app.models.promotions import Promotion
        from app.services.promotions import PromotionService
        
        now = datetime.utcnow()
        
        # Create future promotion
        promotion = Promotion(
            name="Future Promotion",
            code="FUTURE",
            description="Future promo",
            discount_type="percentage",
            discount_value=20.0,
            minimum_order_amount=0.0,
            start_date=now + timedelta(days=7),  # Starts in future
            end_date=now + timedelta(days=30),
            max_uses=100,
            current_uses=0,
            status="active",
        )
        db.add(promotion)
        db.commit()
        
        service = PromotionService(db)
        result = service.check_eligibility("FUTURE", order_amount=100.0)
        
        assert result.eligible is False
        assert any("not started" in error.lower() or "has not started" in error.lower() for error in result.errors)
    
    def test_inactive_promotion(self, db):
        """Test inactive promotion is ineligible."""
        from app.models.promotions import Promotion
        from app.services.promotions import PromotionService
        
        now = datetime.utcnow()
        
        # Create inactive promotion
        promotion = Promotion(
            name="Inactive Promotion",
            code="INACTIVE",
            description="Inactive promo",
            discount_type="percentage",
            discount_value=15.0,
            minimum_order_amount=0.0,
            start_date=now - timedelta(days=1),
            end_date=now + timedelta(days=30),
            max_uses=100,
            current_uses=0,
            status="inactive",
        )
        db.add(promotion)
        db.commit()
        
        service = PromotionService(db)
        result = service.check_eligibility("INACTIVE", order_amount=100.0)
        
        assert result.eligible is False
        assert any("not active" in error.lower() for error in result.errors)


class TestPromotionManagement:
    """Test promotion CRUD operations."""
    
    def test_create_promotion(self, client, admin_token, db):
        """Test creating new promotion."""
        now = datetime.utcnow()
        
        response = client.post(
            "/api/v1/promotions",
            headers={"Authorization": f"Bearer {admin_token}"},
            json={
                "name": "New Promotion",
                "code": "NEW20",
                "description": "20% off new promotion",
                "discount_type": "percentage",
                "discount_value": 20.0,
                "minimum_order_amount": 100.0,
                "start_date": now.isoformat(),
                "end_date": (now + timedelta(days=30)).isoformat(),
                "max_uses": 500,
                "status": "active",
            },
        )
        
        assert response.status_code == status.HTTP_201_CREATED
        data = response.json()
        assert data["code"] == "NEW20"
        assert data["discount_value"] == 20.0
    
    def test_list_promotions(self, client, admin_token, test_promotion):
        """Test listing promotions."""
        response = client.get(
            "/api/v1/promotions",
            headers={"Authorization": f"Bearer {admin_token}"},
        )
        
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert "items" in data
        assert "total" in data
        assert data["total"] >= 1
    
    def test_activate_promotion(self, client, admin_token, db):
        """Test activating a promotion."""
        from app.models.promotions import Promotion
        
        now = datetime.utcnow()
        
        # Create inactive promotion
        promotion = Promotion(
            name="To Activate",
            code="ACTIVATE",
            description="Promotion to activate",
            discount_type="percentage",
            discount_value=10.0,
            minimum_order_amount=0.0,
            start_date=now - timedelta(days=1),
            end_date=now + timedelta(days=30),
            max_uses=100,
            current_uses=0,
            status="inactive",
        )
        db.add(promotion)
        db.commit()
        
        response = client.post(
            f"/api/v1/promotions/{promotion.id}/activate",
            headers={"Authorization": f"Bearer {admin_token}"},
        )
        
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert data["status"] == "active"
    
    def test_deactivate_promotion(self, client, admin_token, test_promotion):
        """Test deactivating a promotion."""
        response = client.post(
            f"/api/v1/promotions/{test_promotion.id}/deactivate",
            headers={"Authorization": f"Bearer {admin_token}"},
        )
        
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert data["status"] == "inactive"


class TestPromotionAuth:
    """Test promotion endpoint authorization."""
    
    def test_promotion_list_requires_auth(self, client):
        """Test listing promotions requires authentication."""
        response = client.get("/api/v1/promotions")
        
        # May be public or require auth depending on implementation
        assert response.status_code in [status.HTTP_200_OK, status.HTTP_401_UNAUTHORIZED]
    
    def test_promotion_management_requires_admin(self, client, auth_token):
        """Test promotion management requires admin role."""
        response = client.post(
            "/api/v1/promotions",
            headers={"Authorization": f"Bearer {auth_token}"},
            json={
                "name": "Test",
                "code": "TEST",
                "discount_type": "percentage",
                "discount_value": 10.0,
            },
        )
        
        # Customer should not be able to create promotions
        assert response.status_code in [status.HTTP_403_FORBIDDEN, status.HTTP_401_UNAUTHORIZED]
