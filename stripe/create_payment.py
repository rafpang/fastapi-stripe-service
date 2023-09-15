from fastapi import APIRouter, HTTPException
from db.db_init import SessionLocal
from request_model.request_models import PaymentRequest
from db.db_models import Payment
from celery.celery_task import process_successful_payment

router = APIRouter(prefix="/payment")


@router.post("/create-payment")
def create_payment(payment_request: PaymentRequest):
    try:
        db = SessionLocal()
        payment = Payment(
            amount=payment_request.amount,
            currency=payment_request.currency,
            email=payment_request.email,
            status="pending",
        )
        db.add(payment)
        db.commit()
        db.refresh(payment)
        payment_id = payment.id

        payment.status = "succeeded"
        db.commit()

        process_successful_payment.apply_async(args=[payment_id, payment_request.email])

        return "Payment processing started asynchronously"
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Payment Error: {str(e)}")
