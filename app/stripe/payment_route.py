from fastapi import APIRouter, HTTPException
from app.stripe.stripe_checkout import run_stripe_checkout_session
from fastapi import Body
from app.request_model.request_models import PaymentRequest

from app.celery_and_tasks.process_successful_payment_task import (
    process_successful_payment,
)


router = APIRouter(prefix="/payment")


@router.post("/checkout")
def create_payment(
    payment_request: PaymentRequest,
):
    try:
        price_id = payment_request.price_id
        quantity = payment_request.quantity
        email = payment_request.email
        payer = payment_request.payer
        seat_location = payment_request.seat_location
        show_time = payment_request.show_time
        payment_task_response = run_stripe_checkout_session(
            price_id=price_id,
            quantity=quantity,
            email=email,
            payer=payer,
            seat_location=seat_location,
            show_time=show_time,
        )

        # process_successful_payment.apply_async(args=[payment_id, payment_request.email])
        return {
            "payment_id": price_id,
            "status": "successful",
            "session_url": payment_task_response["session_url"],
            "session_id": payment_task_response["session_id"],
        }
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Payment Error: {str(e)}")
