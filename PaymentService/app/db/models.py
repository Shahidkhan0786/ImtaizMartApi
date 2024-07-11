from sqlmodel import SQLModel,Field , Relationship
from sqlalchemy import Column,DateTime,Enum as SQLAlchemyEnum,String
from datetime import datetime
from typing import Optional
from app.enums.enums import PaymentStatusEnum

class Transaction(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    customer_id: Optional[int] = Field(default=None)
    order_id: Optional[int] = Field(default=None)
    description: str = Field(default="", max_length=500)
    total_amount : float = Field(default=0)
    payment_status: PaymentStatusEnum = Field(default=PaymentStatusEnum.PENDING,sa_column=Column(SQLAlchemyEnum(PaymentStatusEnum)))
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

    # # orders: relationship("Order", backref="shipping_address")

    class Config:
        orm_mode = True




