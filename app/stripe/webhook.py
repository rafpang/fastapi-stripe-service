from app.celery_and_tasks.process_successful_payment_task import (
    process_successful_payment,
)
from .stripe_init import get_stripe_instance

from fastapi import APIRouter, Request, Depends


router = APIRouter(prefix="/webhook")


@router.post("/stripe-webhook")
async def stripe_webhook(request: Request, stripe=Depends(get_stripe_instance)):
    try:
        event = await request.json()
        webhook_secret = "your_webhook_secret_key"

        stripe_event = stripe.Webhook.construct_event(
            payload=event, secret=webhook_secret
        )

        if stripe_event.type == "payment_intent.succeeded":
            payment_intent = stripe_event.data.object
            payment_id = payment_intent.metadata.get("payment_id")
            email = payment_intent.metadata.get("email")

        process_successful_payment.apply_async(args=[payment_id, email])

        return "Webhook processed successfully"
    except Exception as e:
        return f"Webhook Error: {str(e)}"
