from pydantic import BaseModel


class PaymentRequest(BaseModel):
    amount: int
    price_id: str
    quantity: int
    audience: str
    email: str
