from sqlmodel import SQLModel,Field , Relationship
from sqlalchemy import Column,DateTime,Enum as SQLAlchemyEnum,String
from datetime import datetime
from typing import Optional
from app.enums.status_enum import StatusEnum

class StockLevel(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    product_id: Optional[int] = Field(default=None)
    quantity: int = Field(default=0)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
    class Config:
        orm_mode = True
        

class InventoryUpdate(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    product_id: int = Field(default=None)
    change: int  # Positive for addition, negative for removal
    updated_by: str  # User who made the update
    reason: str  # Reason for the update
    created_at: datetime = Field(default_factory=datetime.utcnow)
    
    class Config:
        orm_mode = True
        


