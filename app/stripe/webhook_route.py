from app.celery_and_tasks.process_successful_payment_task import (
    process_successful_payment,
)
from .stripe_init import get_stripe_instance

from fastapi import APIRouter, Request, Depends
from dotenv import load_dotenv
import os

load_dotenv()

router = APIRouter(prefix="/webhook")
# metadata={
#                 "payer": payer,
#                 "email": email,
#                 "quantity": quantity,
#                 "seat_location": seat_location,
#                 "show_time": show_time,
#             },


@router.post("/stripe-webhook")
async def stripe_webhook(request: Request, stripe=Depends(get_stripe_instance)):
    try:
        event = await request.json()
        webhook_secret = os.environ.get("STRIPE_WEBHOOK_SECRET")

        stripe_event = stripe.Webhook.construct_event(
            payload=event, secret=webhook_secret
        )

        #   metadata={
        #         "payer": payer,
        #         "email": email,
        #         "quantity": quantity,
        #         "seat_location": seat_location,
        #         "show_time": show_time,
        #     },

        if stripe_event.type == "payment_intent.succeeded":
            event_id = stripe_event.data.object.id
            payment_intent_metadata = stripe_event.data.object.metadata
            payee = payment_intent_metadata.get("payer")
            email = payment_intent_metadata.get("email")
            quantity = payment_intent_metadata.get("quantity")
            seat_location = payment_intent_metadata.get("seat_location")
            show_time = payment_intent_metadata.get("show_time")
            print(event_id, payee, email, quantity, seat_location, show_time)

        # process_successful_payment.apply_async(args=[payment_id, email])

        return "Webhook processed successfully"
    except Exception as e:
        return f"Webhook Error: {str(e)}"
