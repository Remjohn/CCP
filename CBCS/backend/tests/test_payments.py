import pytest
from backend.core.payments import payments

def test_payment_split_success():
    # $100.00 Subscription
    result = payments.process_subscription(
        user_id="u1", 
        amount_cents=10000, 
        coach_stripe_id="acct_123"
    )
    
    assert result.success is True
    assert result.amount_total == 10000
    assert result.amount_platform == 500 # $5.00 fixed fee
    assert result.amount_coach == 9500   # $95.00 remainder

def test_payment_split_low_amount():
    # $4.00 Subscription (Less than fee)
    result = payments.process_subscription(
        user_id="u2", 
        amount_cents=400, 
        coach_stripe_id="acct_123"
    )
    
    assert result.success is False
    assert result.error_message == "Amount less than platform fee"
