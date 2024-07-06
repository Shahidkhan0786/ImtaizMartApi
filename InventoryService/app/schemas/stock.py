from typing import Optional
from datetime import datetime
from pydantic import BaseModel
from sqlmodel import SQLModel, Field


class StockBase(SQLModel):
    product_id: Optional[int]
    quantity: int
    low_stock_threshold: int


class StockCreate(StockBase):
    pass


class StockRead(StockBase):
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True


class StockUpdate(SQLModel):
    product_id: Optional[int]
    quantity: Optional[int]
    low_stock_threshold: Optional[int]
