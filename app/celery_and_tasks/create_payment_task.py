from .celery_init import celery
from app.db.db_init import SessionLocal
from app.db.db_models import Payment
from app.db.db_init import SessionLocal
from app.request_model.request_models import PaymentRequest
from app.stripe.stripe_init import get_stripe_instance


@celery.task
def create_payment_task(payment_request: PaymentRequest):
    try:
        stripe = get_stripe_instance()
        session = stripe.checkout.Session.create(
            payment_method_types=["card", "paynow"],
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
