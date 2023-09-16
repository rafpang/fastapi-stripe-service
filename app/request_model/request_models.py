from pydantic import BaseModel


class PaymentRequest(BaseModel):
    amount: int
    audience: str
    currency: str
    email: str
