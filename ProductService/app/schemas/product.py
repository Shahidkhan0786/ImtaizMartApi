from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class ProductBase(BaseModel):
    categoryId: Optional[int] = None
    brandId: Optional[int] = None
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

