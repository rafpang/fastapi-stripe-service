import stripe
from dotenv import load_dotenv
import os

load_dotenv()


# Run in everytime stripe instance is required
def get_stripe_instance():
    stripe.api_key = os.environ.get("STRIPE_SECRET_KEY")
    return stripe
