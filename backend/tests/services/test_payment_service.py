"""Tests for payment service mock implementation."""

import pytest
from decimal import Decimal
from app.services.payment_service import (
    PaymentService,
    MockPaymentProvider,
    PaymentOutcome,
    get_payment_service
)


class TestMockPaymentProvider:
    """Test mock payment provider behavior."""
    
    def test_successful_payment(self):
        """Test successful payment submission."""
        provider = MockPaymentProvider()
        outcome = provider.submit_payment(
            amount=Decimal("50.00"),
            currency="USD",
            order_id=1,
            payment_method_token="mock_token_123"
        )
        
        assert outcome.status == "succeeded"
        assert outcome.transaction_id.startswith("mock_success_")
        assert outcome.error_message is None
        assert outcome.raw_response["mock"] is True
    
    def test_declined_payment_low_amount(self):
        """Test declined payment when amount too low."""
        provider = MockPaymentProvider()
        outcome = provider.submit_payment(
            amount=Decimal("0.50"),
            currency="USD",
            order_id=2,
            payment_method_token="mock_token_123"
        )
        
        assert outcome.status == "failed"
        assert outcome.transaction_id.startswith("mock_declined_")
        assert "insufficient funds" in outcome.error_message.lower()
    
    def test_timeout_payment_high_amount(self):
        """Test timeout simulation for high amounts."""
        provider = MockPaymentProvider()
        outcome = provider.submit_payment(
            amount=Decimal("1500.00"),
            currency="USD",
            order_id=3,
            payment_method_token="mock_token_123"
        )
        
        assert outcome.status == "pending"
        assert outcome.transaction_id.startswith("mock_timeout_")
        assert "timeout" in outcome.error_message.lower()


class TestPaymentService:
    """Test payment service orchestration."""
    
    def test_process_successful_payment(self):
        """Test processing successful payment."""
        service = PaymentService(provider=MockPaymentProvider())
        outcome = service.process_payment(
            amount=Decimal("100.00"),
            currency="USD",
            order_id=1,
            payment_method_token="mock_token_123"
        )
        
        assert outcome.status == "succeeded"
        assert outcome.transaction_id is not None
    
    def test_process_payment_invalid_amount(self):
        """Test payment with invalid amount raises error."""
        service = PaymentService(provider=MockPaymentProvider())
        
        with pytest.raises(ValueError, match="must be positive"):
            service.process_payment(
                amount=Decimal("0.00"),
                currency="USD",
                order_id=1,
                payment_method_token="mock_token_123"
            )
    
    def test_process_payment_negative_amount(self):
        """Test payment with negative amount raises error."""
        service = PaymentService(provider=MockPaymentProvider())
        
        with pytest.raises(ValueError, match="must be positive"):
            service.process_payment(
                amount=Decimal("-10.00"),
                currency="USD",
                order_id=1,
                payment_method_token="mock_token_123"
            )
    
    def test_get_payment_service_singleton(self):
        """Test get_payment_service returns service instance."""
        service = get_payment_service()
        assert isinstance(service, PaymentService)
        assert isinstance(service.provider, MockPaymentProvider)


class TestPaymentOutcome:
    """Test payment outcome data structure."""
    
    def test_create_successful_outcome(self):
        """Test creating successful payment outcome."""
        outcome = PaymentOutcome(
            status="succeeded",
            transaction_id="txn_123",
            raw_response={"amount": "50.00"}
        )
        
        assert outcome.status == "succeeded"
        assert outcome.transaction_id == "txn_123"
        assert outcome.error_message is None
        assert outcome.timestamp is not None
    
    def test_create_failed_outcome(self):
        """Test creating failed payment outcome."""
        outcome = PaymentOutcome(
            status="failed",
            transaction_id="txn_456",
            error_message="Card declined"
        )
        
        assert outcome.status == "failed"
        assert outcome.error_message == "Card declined"
        assert outcome.timestamp is not None
