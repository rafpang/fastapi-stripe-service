import stripe
from dotenv import load_dotenv
import os

load_dotenv()


def get_stripe_instance():
    stripe.api_key = os.environ.get("STRIPE_SECRET_KEY")
    return stripe
