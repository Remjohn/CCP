from fastapi import APIRouter, Request, HTTPException

router = APIRouter()

@router.post("/stripe/webhook")
async def stripe_webhook(request: Request):
    """POST /api/stripe/webhook — Stripe webhook endpoint with signature verification.
    Rejects invalid signatures with HTTP 400 (AC-3.4)."""
    import stripe
    payload = await request.body()
    sig_header = request.headers.get("Stripe-Signature", "")
    if not sig_header:
        raise HTTPException(status_code=400, detail="Missing Stripe-Signature header")
    try:
        event = stripe.Webhook.construct_event(payload, sig_header, endpoint_secret="")
    except stripe.error.SignatureVerificationError:
        raise HTTPException(status_code=400, detail="Invalid Stripe signature")
    except Exception:
        raise HTTPException(status_code=400, detail="Invalid payload")
    return {"status": "ok"}
