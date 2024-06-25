from typing import Optional
from pydantic import BaseModel,validator
from datetime import datetime
from app.enums.status_enum import StatusEnum

class BrandBase(BaseModel):
    title: str
    description: Optional[str] = None
    image_url: Optional[str] = None
    status: Optional[StatusEnum] = StatusEnum.activate

class BrandCreate(BrandBase):
    pass

class BrandRead(BrandBase):
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

class BrandUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    image_url: Optional[str] = None
    status: Optional[StatusEnum] = None