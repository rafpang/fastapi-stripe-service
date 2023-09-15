from fastapi import APIRouter, HTTPException, Depends
from db.db_init import SessionLocal
from request_model.request_models import PaymentRequest
from db.db_models import Payment
from celery.celery_task import process_successful_payment
from stripe import checkout
from .stripe_init import get_stripe_api_key

router = APIRouter(prefix="/payment")


@router.post(
    "/create-payment",
)
def create_payment(payment_request: PaymentRequest, stripe=Depends(get_stripe_api_key)):
    try:
        stripe.checkout.Session.create(
            payment_method_types=["card"],
            line_items=[
                {
                    "price": "priceId",  # Replace with the actual price ID from Stripe
                    "quantity": 1,
                }
            ],
            mode="payment",
            success_url="http://localhost:3000/success",  # Replace with your success URL
            cancel_url="http://localhost:3000/cancel",  # Replace with your cancel URL
        )

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
