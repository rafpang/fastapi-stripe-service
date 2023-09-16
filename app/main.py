from fastapi import FastAPI

# from email.mime.multipart import MIMEMultipart
# from email.mime.text import MIMEText
# from email.mime.image import MIMEImage
# import qrcode

# from io import BytesIO

# import requests
from .db.db_init import engine
from .db.db_models import Base
from .stripe.payment_route import router as payment_router
from .stripe.webhook_route import router as webhook_router

Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(payment_router)
app.include_router(webhook_router)

# Define the send_email_with_qr functioncvff
# def send_email_with_qr(recipient_email, payment_id):
#     MAILGUN_DOMAIN = "HELLO"
#     MAILGUN_API_KEY = "API KEY"
#     try:
#         # Generate QR code with the payment ID as the data
#         qr = qrcode.QRCode(
#             version=1,
#             error_correction=qrcode.constants.ERROR_CORRECT_L,
#             box_size=10,
#             border=4,
#         )
#         qr.add_data(str(payment_id))
#         qr.make(fit=True)
#         qr_img = qr.make_image(fill_color="black", back_color="white")

#         # Create a BytesIO object to store the QR code image
#         qr_byteio = BytesIO()
#         qr_img.save(qr_byteio, format="PNG")
#         qr_byteio.seek(0)

#         # Create an email message
#         msg = MIMEMultipart()
#         msg["From"] = "your_email@gmail.com"  # Replace with your email
#         msg["To"] = recipient_email
#         msg["Subject"] = "Payment Confirmation"

#         # Email body with a thank-you message
#         body = """
#         Thank you for the payment!
#         """
#         msg.attach(MIMEText(body, "plain"))

#         img = MIMEImage(qr_byteio.read())
#         img.add_header("Content-Disposition", "attachment", filename="qrcode.png")
#         msg.attach(img)

#         response = requests.post(
#             f"https://api.mailgun.net/v3/{MAILGUN_DOMAIN}/messages",
#             auth=("api", MAILGUN_API_KEY),
#             files=[("attachment", ("qrcode.png", qr_byteio.getvalue()))],
#             data={
#                 "from": "your_email@gmail.com",
#                 "to": recipient_email,
#                 "subject": "Payment Confirmation",
#                 "text": "Thank you for the payment!",
#             },
#         )
#         if response.status_code == 200:
#             print("Email sent successfully!")
#         else:
#             print("Email sending failed with status code:", response.status_code)
#     except Exception as e:
#         print("Email sending failed:", str(e))


if __name__ == "__main__":
    import uvicorn

    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
