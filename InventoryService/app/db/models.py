from sqlmodel import SQLModel,Field , Relationship
from sqlalchemy import Column,DateTime,Enum as SQLAlchemyEnum,String
from datetime import datetime
from typing import Optional
from app.enums.enums import TransactionTypeEnum

class Stock(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    product_id: Optional[int] = Field(default=None)
    quantity: int = Field(default=0)
    low_stock_threshold : int = Field(default=10)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
    class Config:
        orm_mode = True
        

class Inventory(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    product_id: int = Field(default=None)
    title: Optional[str] = Field(default=None)
    quantity: int = Field(default=0)
    description: str = Field(default=None)
    transaction_type: TransactionTypeEnum = Field(default=TransactionTypeEnum.IN,sa_column=Column(SQLAlchemyEnum(TransactionTypeEnum)))
    updated_by: Optional[int] = Field(default=None) # User who made the update
    details : str  # Reason for the update
    created_at: datetime = Field(default_factory=datetime.utcnow)
    
    class Config:
        orm_mode = True
        


