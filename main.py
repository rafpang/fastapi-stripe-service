from .request_models import PaymentRequest
from .db_models import Payment
from .celery_init import celery
from .db_init import SessionLocal

from fastapi import FastAPI, HTTPException, Request

from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
import qrcode
from PIL import Image
from io import BytesIO
import stripe
import requests


app = FastAPI()


stripe.api_key = "your_stripe_secret_key"


# Pydantic model for payment requests


# Celery task for processing successful payments
@celery.task
def process_successful_payment(payment_id, email):
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


# Define the send_email_with_qr function
def send_email_with_qr(recipient_email, payment_id):
    MAILGUN_DOMAIN = "HELLO"
    MAILGUN_API_KEY = "API KEY"
    try:
        # Generate QR code with the payment ID as the data
        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_L,
            box_size=10,
            border=4,
        )
        qr.add_data(str(payment_id))
        qr.make(fit=True)
        qr_img = qr.make_image(fill_color="black", back_color="white")

        # Create a BytesIO object to store the QR code image
        qr_byteio = BytesIO()
        qr_img.save(qr_byteio, format="PNG")
        qr_byteio.seek(0)

        # Create an email message
        msg = MIMEMultipart()
        msg["From"] = "your_email@gmail.com"  # Replace with your email
        msg["To"] = recipient_email
        msg["Subject"] = "Payment Confirmation"

        # Email body with a thank-you message
        body = """
        Thank you for the payment!
        """
        msg.attach(MIMEText(body, "plain"))

        # Attach the QR code image to the email
        img = MIMEImage(qr_byteio.read())
        img.add_header("Content-Disposition", "attachment", filename="qrcode.png")
        msg.attach(img)

        # Send the email using Mailgun
        response = requests.post(
            f"https://api.mailgun.net/v3/{MAILGUN_DOMAIN}/messages",
            auth=("api", MAILGUN_API_KEY),
            files=[("attachment", ("qrcode.png", qr_byteio.getvalue()))],
            data={
                "from": "your_email@gmail.com",
                "to": recipient_email,
                "subject": "Payment Confirmation",
                "text": "Thank you for the payment!",
            },
        )
        if response.status_code == 200:
            print("Email sent successfully!")
        else:
            print("Email sending failed with status code:", response.status_code)
    except Exception as e:
        print("Email sending failed:", str(e))


# Endpoint to create payments and initiate processing
@app.post("/create-payment")
def create_payment(payment_request: PaymentRequest):
    try:
        # Implement the payment processing logic here
        # For example, create a payment record in the database
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

        # Simulate a payment success (Replace with actual payment logic)
        # In a real scenario, you would interact with Stripe or a payment gateway.
        payment.status = "succeeded"
        db.commit()

        # Enqueue the Celery task to process the successful payment
        process_successful_payment.apply_async(args=[payment_id, payment_request.email])

        return "Payment processing started asynchronously"
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Payment Error: {str(e)}")


# Stripe webhook handling endpoint
@app.post("/stripe-webhook")
async def stripe_webhook(request: Request):
    try:
        event = await request.json()
        webhook_secret = (
            "your_webhook_secret_key"  # Replace with your webhook secret key
        )

        # Verify the webhook signature
        stripe_event = stripe.Webhook.construct_event(
            payload=event, secret=webhook_secret
        )

        if stripe_event.type == "payment_intent.succeeded":
            payment_intent = stripe_event.data.object
            payment_id = payment_intent.metadata.get("payment_id")
            email = payment_intent.metadata.get("email")

        # Enqueue the Celery task to process the successful payment
        process_successful_payment.apply_async(args=[payment_id, email])

        return "Webhook processed successfully"
    except Exception as e:
        return f"Webhook Error: {str(e)}"


if __name__ == "__main__":
    import uvicorn

    # Replace "main:app" with the name of your Python file and FastAPI instance
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
