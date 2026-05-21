from fastapi import APIRouter, Request, HTTPException
from src.ccp.models.billing_models import WalletDisplayPayload

router = APIRouter()


@router.get("/billing/wallet/{coach_id}", response_model=WalletDisplayPayload)
async def get_wallet(coach_id: str):
    """AFFiNE Wallet Block — returns cost breakdown, payment status, and usage history."""
    pass


@router.post("/billing/webhook")
async def billing_webhook(request: Request):
    """Stripe billing webhook handler for subscription lifecycle events.
    Processes: invoice.payment_succeeded, invoice.payment_failed,
    customer.subscription.deleted, customer.subscription.updated."""
    pass


@router.get("/billing/status/{coach_id}")
async def get_billing_status(coach_id: str):
    """Returns current billing status and tier for a coach from Redis cache."""
    pass
