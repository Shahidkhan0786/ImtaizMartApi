from pydantic import BaseModel
from typing import Optional
from datetime import datetime
from app.enums.order_status_enum import OrderStatusEnum

class OrderBase(BaseModel):
    user_id: Optional[int] = None
    order_number: int
    total_price: float
    title: str
    description: str
    status: str
    # image_url: Optional[str] = None
    # quantity: Optional[int] = None
    # rating: Optional[float] = None

class OrderCreate(OrderBase):
    pass

class OrderRead(OrderBase):
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True

# class ProductUpdate(BaseModel):
#     category_id: Optional[int] = None
#     brand_id: Optional[int] = None
#     # user_id: Optional[int] = None
#     title: str
#     description: str
#     price: float
#     image_url: Optional[str] = None
#     quantity: Optional[int] = None
#     # rating: Optional[float] = None


# class User(BaseModel):
#     first_name: str
#     last_name: str | None = None
#     email: str

# class ProductDetail(ProductBase):
#     id: int
#     owner:User
#     created_at: datetime
#     updated_at: datetime

#     class Config:
#         orm_mode = True

