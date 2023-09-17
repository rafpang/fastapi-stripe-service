from app.db.db_init import SessionLocal
from app.db.db_models import Payment
from app.db.db_init import SessionLocal
from app.stripe.stripe_init import get_stripe_instance
from app.request_model.request_models import PaymentRequest


def run_stripe_checkout_session(
    price_id: str,
    quantity: int,
    email: str,
    payer: str,
    seat_location: str,
    show_time: str,
):
    try:
        stripe = get_stripe_instance()

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
            metadata={
                "payer": payer,
                "email": email,
                "quantity": quantity,
                "seat_location": seat_location,
                "show_time": show_time,
            },
        )
        # db = SessionLocal()
        # payment = Payment(
        #     amount=payment_request.amount,
        #     currency=payment_request.currency,
        #     email=payment_request.email,
        #     status="pending",
        # )
        # db.add(payment)
        # db.commit()
        # db.refresh(payment)
        # payment_id = payment.id

        return {"session_id": session.id, "session_url": session.url, "payer": payer}
    except Exception as e:
        return {"error": str(e)}
