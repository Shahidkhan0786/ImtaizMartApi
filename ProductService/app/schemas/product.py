from pydantic import BaseModel
from typing import Optional
from datetime import datetime
from app.enums.status_enum import StatusEnum
class ProductBase(BaseModel):
    category_id: Optional[int] = None
    brand_id: Optional[int] = None
    user_id: Optional[int] = None
    title: str
    description: str
    price: float
    image_url: Optional[str] = None
    quantity: Optional[int] = None
    rating: Optional[float] = None

class ProductCreate(ProductBase):
    pass

class ProductRead(ProductBase):
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True

class ProductUpdate(BaseModel):
    category_id: Optional[int] = None
    brand_id: Optional[int] = None
    # user_id: Optional[int] = None
    title: str
    description: str
    price: float
    image_url: Optional[str] = None
    quantity: Optional[int] = None
    # rating: Optional[float] = None


class User(BaseModel):
    first_name: str
    last_name: str | None = None
    email: str

class ProductDetail(ProductBase):
    id: int
    owner:User
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True

