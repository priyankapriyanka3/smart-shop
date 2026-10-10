"""Payment service with mock implementation for development.

This module provides payment processing functionality for Smart Shop.
In development, it uses a mock payment provider that simulates payment outcomes.
In production, replace MockPaymentProvider with a real payment provider adapter.

Payment Provider Integration Requirements:
- Implement PaymentProvider interface with submit_payment method
- Return PaymentOutcome with status, transaction_id, and error_message
- Handle network errors and timeouts gracefully
- Log all payment attempts for audit trail
- Never store raw card details (use tokenized payments)

Required Environment Variables (Production):
- PAYMENT_PROVIDER_URL: Payment gateway API endpoint
- PAYMENT_PROVIDER_API_KEY: Authentication key for payment gateway
- PAYMENT_TIMEOUT_SECONDS: Request timeout (default: 30)
"""

import os
import logging
from typing import Optional
from datetime import datetime
from decimal import Decimal
import uuid

logger = logging.getLogger(__name__)


class PaymentOutcome:
    """Payment result with status and transaction details."""
    
    def __init__(
        self,
        status: str,
        transaction_id: Optional[str] = None,
        error_message: Optional[str] = None,
        raw_response: Optional[dict] = None
    ):
        """Initialize payment outcome.
        
        Args:
            status: Payment status (succeeded, failed, pending)
            transaction_id: Provider transaction identifier
            error_message: Error description if status is failed
            raw_response: Full provider response for debugging
        """
        self.status = status
        self.transaction_id = transaction_id
        self.error_message = error_message
        self.raw_response = raw_response
        self.timestamp = datetime.utcnow()


class PaymentProvider:
    """Abstract payment provider interface."""
    
    def submit_payment(
        self,
        amount: Decimal,
        currency: str,
        order_id: int,
        payment_method_token: str
    ) -> PaymentOutcome:
        """Submit payment to provider.
        
        Args:
            amount: Payment amount
            currency: Currency code (USD, EUR, etc.)
            order_id: Smart Shop order ID for reference
            payment_method_token: Tokenized payment method
            
        Returns:
            PaymentOutcome with status and transaction details
        """
        raise NotImplementedError("Subclasses must implement submit_payment")


class MockPaymentProvider(PaymentProvider):
    """Mock payment provider for development and testing.
    
    Simulates payment outcomes based on amount thresholds:
    - Amount < $1.00: Simulates declined card
    - Amount >= $1000.00: Simulates processing timeout
    - All other amounts: Simulates successful payment
    
    Real payment providers will replace this with actual API integration.
    """
    
    def submit_payment(
        self,
        amount: Decimal,
        currency: str,
        order_id: int,
        payment_method_token: str
    ) -> PaymentOutcome:
        """Simulate payment submission.
        
        Args:
            amount: Payment amount
            currency: Currency code (default USD in mock)
            order_id: Smart Shop order ID
            payment_method_token: Simulated payment token
            
        Returns:
            PaymentOutcome with simulated result
        """
        logger.info(
            f"Mock payment submission: order_id={order_id}, "
            f"amount={amount} {currency}, token={payment_method_token[:8]}..."
        )
        
        # Simulate different outcomes based on amount
        if amount < Decimal("1.00"):
            transaction_id = f"mock_declined_{uuid.uuid4().hex[:8]}"
            logger.warning(f"Mock payment declined: {transaction_id}")
            return PaymentOutcome(
                status="failed",
                transaction_id=transaction_id,
                error_message="Card declined - insufficient funds (mock)",
                raw_response={"mock": True, "reason": "amount_too_low"}
            )
        
        if amount >= Decimal("1000.00"):
            transaction_id = f"mock_timeout_{uuid.uuid4().hex[:8]}"
            logger.warning(f"Mock payment timeout: {transaction_id}")
            return PaymentOutcome(
                status="pending",
                transaction_id=transaction_id,
                error_message="Payment provider timeout (mock)",
                raw_response={"mock": True, "reason": "simulated_timeout"}
            )
        
        # Successful payment
        transaction_id = f"mock_success_{uuid.uuid4().hex[:8]}"
        logger.info(f"Mock payment succeeded: {transaction_id}")
        return PaymentOutcome(
            status="succeeded",
            transaction_id=transaction_id,
            raw_response={
                "mock": True,
                "order_id": order_id,
                "amount": str(amount),
                "currency": currency
            }
        )


class PaymentService:
    """Payment service orchestrating payment provider interactions."""
    
    def __init__(self, provider: Optional[PaymentProvider] = None):
        """Initialize payment service with provider.
        
        Args:
            provider: Payment provider implementation (defaults to mock)
        """
        if provider is None:
            # Default to mock provider in development
            provider = MockPaymentProvider()
            logger.info("Using MockPaymentProvider (development mode)")
        self.provider = provider
    
    def process_payment(
        self,
        amount: Decimal,
        currency: str,
        order_id: int,
        payment_method_token: str
    ) -> PaymentOutcome:
        """Process payment for order.
        
        Args:
            amount: Payment amount
            currency: Currency code
            order_id: Smart Shop order ID
            payment_method_token: Tokenized payment method
            
        Returns:
            PaymentOutcome with result
            
        Raises:
            ValueError: If amount is invalid
            RuntimeError: If payment provider fails catastrophically
        """
        if amount <= 0:
            raise ValueError("Payment amount must be positive")
        
        try:
            outcome = self.provider.submit_payment(
                amount=amount,
                currency=currency,
                order_id=order_id,
                payment_method_token=payment_method_token
            )
            
            # Log outcome for audit trail
            logger.info(
                f"Payment processed: order_id={order_id}, "
                f"status={outcome.status}, "
                f"transaction_id={outcome.transaction_id}"
            )
            
            return outcome
            
        except Exception as e:
            logger.error(f"Payment provider error: {e}", exc_info=True)
            # Return failed outcome instead of raising
            return PaymentOutcome(
                status="failed",
                error_message=f"Payment provider error: {str(e)}"
            )


# Global payment service instance (can be injected for testing)
payment_service = PaymentService()


def get_payment_service() -> PaymentService:
    """Get payment service instance.
    
    Returns:
        PaymentService instance (uses mock provider in development)
    """
    return payment_service
