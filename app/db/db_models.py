from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base


Base = declarative_base()


class Payment(Base):
    __tablename__ = "payments"
    id = Column(String, primary_key=True, index=True)
    payee = Column(String)
    num_tickets = Column(Integer)
    seat_details = Column(String)
    email = Column(String)
    amount = Column(Integer)
