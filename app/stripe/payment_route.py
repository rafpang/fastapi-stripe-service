from fastapi import APIRouter, HTTPException
from app.stripe.stripe_checkout import run_stripe_checkout_session

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
        payment_task_response = run_stripe_checkout_session(payment_request)
        payment_id = payment_task_response["payment_id"]
        # process_successful_payment.apply_async(args=[payment_id, payment_request.email])
        return {"payment_id": payment_id, "status": "successful"}
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Payment Error: {str(e)}")
