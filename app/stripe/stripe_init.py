import stripe


def get_stripe_instance():
    stripe.api_key = "your_stripe_secret_key"
    return stripe
