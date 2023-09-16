from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base


Base = declarative_base()


class Payment(Base):
    __tablename__ = "payments"
    id = Column(Integer, primary_key=True, index=True)
    payee = Column(String)
    seat_details = Column(String)
    email = Column(String)
    amount = Column(Integer)
