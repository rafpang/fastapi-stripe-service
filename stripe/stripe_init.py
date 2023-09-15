import stripe


def get_stripe_api_key():
    stripe.api_key = (
        "your_stripe_secret_key"  # Replace with your actual Stripe secret key
    )
    return stripe
