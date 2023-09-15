from celery.celery_task import process_successful_payment
from fastapi import APIRouter, Request
from stripe.stripe_init import stripe

router = APIRouter(prefix="/webhook")


@router.post("/stripe-webhook")
async def stripe_webhook(request: Request):
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
