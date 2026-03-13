from pydantic import BaseModel
from typing import Optional

class PaymentResult(BaseModel):
    success: bool
    transaction_id: str
    amount_total: int
    amount_coach: int
    amount_platform: int
    error_message: Optional[str] = None

class PaymentService:
    def __init__(self):
        self.platform_fee_cents = 500 # $5.00

    def process_subscription(self, user_id: str, amount_cents: int, coach_stripe_id: str) -> PaymentResult:
        """
        Simulates a Stripe Connect Destination Charge.
        """
        # Mock Stripe Logic
        if amount_cents < self.platform_fee_cents:
            return PaymentResult(
                success=False,
                transaction_id="",
                amount_total=0,
                amount_coach=0,
                amount_platform=0,
                error_message="Amount less than platform fee"
            )

        # Calculate Split
        amount_platform = self.platform_fee_cents
        amount_coach = amount_cents - amount_platform

        # Mock API Call Success
        import uuid
        transaction_id = f"ch_{uuid.uuid4()}"

        return PaymentResult(
            success=True,
            transaction_id=transaction_id,
            amount_total=amount_cents,
            amount_coach=amount_coach,
            amount_platform=amount_platform
        )

# Global Instance
payments = PaymentService()
