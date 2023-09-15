from .celery_init import celery
from app.db.db_init import SessionLocal
from app.db.db_models import Payment


@celery.task
def process_successful_payment(
    payment_id,
    #    email)
):
    try:
        # Update the database to reflect the successful payment
        db = SessionLocal()
        db_payment = db.query(Payment).filter(Payment.id == payment_id).first()

        if db_payment:
            db_payment.status = "succeeded"
            db.commit()
            db.refresh(db_payment)

            # Send email with QR code
            # send_email_with_qr(email, payment_id)

        return "Payment processed successfully"
    except Exception as e:
        return f"Payment Error: {str(e)}"
