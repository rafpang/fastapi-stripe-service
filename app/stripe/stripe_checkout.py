from app.db.db_init import SessionLocal
from app.db.db_models import Payment
from app.db.db_init import SessionLocal
from app.stripe.stripe_init import get_stripe_instance


def run_stripe_checkout_session(payment_request):
    try:
        stripe = get_stripe_instance()
        price_id = payment_request["price_id"]
        quantity = payment_request["quantity"]
        session = stripe.checkout.Session.create(
            payment_method_types=["card", "paynow"],
            line_items=[
                {
                    "price": price_id,
                    "quantity": quantity,
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
