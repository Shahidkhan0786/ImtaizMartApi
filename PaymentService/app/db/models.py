from sqlmodel import SQLModel,Field , Relationship
from sqlalchemy import Column,DateTime,Enum as SQLAlchemyEnum,String
from datetime import datetime
from typing import Optional
from app.enums.enums import TransactionTypeEnum , OrderStatusEnum ,PaymentTypeEnum


class ShippingAddress(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: Optional[int] = Field(default=None)
    address: str = Field(default="", max_length=500)
    company_name: str | None = Field(default=None, max_length=255)
    city: str = Field(default="", max_length=255)
    state: str | None = Field(default=None, max_length=100) 
    postal_code: str = Field(default="", max_length=20)
    country: str = Field(default="", max_length=255)
    phone_number: str | None = Field(default=None, max_length=20) 
    # Optional: Add a field for a default shipping address flag
    is_default: bool = Field(default=False)

    # orders: relationship("Order", backref="shipping_address")

    class Config:
        orm_mode = True


class Order(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    customer_id: Optional[int] = Field(default=None)
    shipping_address_id: Optional[int] = Field(default=None)
    customer_name: str|None = Field(default=None)
    customer_email: str|None = Field(default=None)
    description: str|None = Field(default=None)
    total_amount : float = Field(default=0)
    payment_type: PaymentTypeEnum = Field(default=PaymentTypeEnum.STRIPE,sa_column=Column(SQLAlchemyEnum(PaymentTypeEnum)))
    order_status: OrderStatusEnum = Field(default=OrderStatusEnum.PENDING,sa_column=Column(SQLAlchemyEnum(OrderStatusEnum)))
    order_date: datetime = Field(default_factory=datetime.utcnow)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
    class Config:
        orm_mode = True
        

class OrderItem(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    order_id: int = Field(default=None)
    product_id: int = Field(default=None)
    title: Optional[str] = Field(default=None)
    quantity: int = Field(default=0)
    item_price : float = Field(default=0)
    total_amount : float = Field(default=0)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

    class Config:
        orm_mode = True
        

        


