from typing import Optional, List
from datetime import datetime
from pydantic import BaseModel
from sqlmodel import SQLModel, Field
from enum import Enum
from app.enums.enums import PaymentTypeEnum , OrderStatusEnum

class ShippingAddressBase(SQLModel):
    # user_id: Optional[int]
    address: str
    company_name: Optional[str]
    city: str
    state: Optional[str]
    postal_code: str
    country: str
    phone_number: Optional[str]
    is_default: bool

class ShippingAddressCreate(ShippingAddressBase):
    pass

class ShippingAddressRead(ShippingAddressBase):
    id: int

    class Config:
        orm_mode = True

class ShippingAddressUpdate(SQLModel):
    # user_id: Optional[int]
    address: Optional[str]
    company_name: Optional[str]
    city: Optional[str]
    state: Optional[str]
    postal_code: Optional[str]
    country: Optional[str]
    phone_number: Optional[str]
    is_default: Optional[bool]

class OrderItemBase(SQLModel):
    product_id: int
    title: Optional[str]
    quantity: int
    item_price: float
    # total_amount: float

class OrderItemCreate(OrderItemBase):
    pass

class OrderItemRead(OrderItemBase):
    id: int

    class Config:
        orm_mode = True

class OrderItemUpdate(SQLModel):
    order_id: Optional[int]
    product_id: Optional[int]
    title: Optional[str]
    quantity: Optional[int]
    item_price: Optional[float]
    total_amount: Optional[float]


class OrderBase(SQLModel):
    # customer_id: Optional[int]
    # shipping_address_id: Optional[int]
    # customer_name: Optional[str]
    # customer_email: Optional[str]
    description: Optional[str]
    total_amount: float
    payment_type: PaymentTypeEnum
    order_status: OrderStatusEnum

class OrderCreate(OrderBase):
    shipping_address: ShippingAddressCreate
    items: List[OrderItemCreate]

class OrderRead(OrderBase):
    id: int
    order_date: datetime
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True

class OrderUpdate(SQLModel):
    customer_id: Optional[int]
    shipping_address_id: Optional[int]
    customer_name: Optional[str]
    customer_email: Optional[str]
    description: Optional[str]
    total_amount: Optional[float]
    payment_type: Optional[PaymentTypeEnum]
    order_status: Optional[OrderStatusEnum]

# class OrderItemBase(SQLModel):
#     order_id: int
#     product_id: int
#     title: Optional[str]
#     quantity: int
#     item_price: float
#     total_amount: float

# class OrderItemCreate(OrderItemBase):
#     pass

# class OrderItemRead(OrderItemBase):
#     id: int

#     class Config:
#         orm_mode = True

# class OrderItemUpdate(SQLModel):
#     order_id: Optional[int]
#     product_id: Optional[int]
#     title: Optional[str]
#     quantity: Optional[int]
#     item_price: Optional[float]
#     total_amount: Optional[float]
