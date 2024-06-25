from typing import Optional, List
from pydantic import BaseModel,validator
from datetime import datetime
from app.enums.status_enum import StatusEnum
from app.schemas.product import ProductRead

class CategoryBase(BaseModel):
    title: str
    description: Optional[str] = None
    image_url: Optional[str] = None
    status: Optional[StatusEnum] = StatusEnum.activate

class CategoryCreate(CategoryBase):
    pass

class CategoryRead(CategoryBase):
    id: int
    created_at: Optional[str] = None
    updated_at: Optional[str] = None

    @validator("created_at", "updated_at", pre=True, always=True)
    def serialize_datetime(cls, value):
        if isinstance(value, datetime):
            return value.isoformat()
        return value

    class Config:
        orm_mode = True

class CategoryUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    image_url: Optional[str] = None
    status: Optional[StatusEnum] = None

class CategoryDetail(CategoryBase):
    id: int
    created_at: datetime
    updated_at: datetime
    products: List[ProductRead] = []

    class Config:
        orm_mode = True