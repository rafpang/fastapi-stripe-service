from fastapi import APIRouter, HTTPException, Depends
from celery.create_payment_task import create_payment_task
from request_model.request_models import PaymentRequest
from db.db_models import Payment
from celery.process_successful_payment_task import process_successful_payment

from .stripe_init import get_stripe_api_key

router = APIRouter(prefix="/payment")


@router.post("/create-payment")
def create_payment(payment_request: PaymentRequest, stripe=Depends(get_stripe_api_key)):
    try:
        payment_task_response = create_payment_task.apply_async(args=[payment_request])
        payment_id = payment_task_response["paymentId"]
        process_successful_payment.apply_async(args=[payment_id, payment_request.email])
        return "Payment processing started asynchronously"
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Payment Error: {str(e)}")
