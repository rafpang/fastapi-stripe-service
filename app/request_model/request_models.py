from pydantic import BaseModel


# seat locatioon may be deprecated
# show time might not be necessary
class PaymentRequest(BaseModel):
    # amount: int
    price_id: str
    quantity: int
    payer: str
    email: str
    seat_location: str
    show_time: str
