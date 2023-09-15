from .celery_init import celery
from db.db_init import SessionLocal
from db.db_models import Payment
from db.db_init import SessionLocal
from request_model import PaymentRequest
from stripe.stripe_init import get_stripe_api_key


@celery.task
def create_payment_task(payment_request: PaymentRequest):
    try:
        stripe = get_stripe_api_key()
        session = stripe.checkout.Session.create(
            payment_method_types=["card"],
            line_items=[
                {
                    "price": "price_123",
                    "quantity": 1,
                }
            ],
            mode="payment",
            success_url="http://localhost:3000/success",
            cancel_url="http://localhost:3000/cancel",
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

        return {"sessionId": session.id, "paymentId": payment_id}
    except Exception as e:
        return {"error": str(e)}
