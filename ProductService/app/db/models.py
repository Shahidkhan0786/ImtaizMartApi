from typing import Optional
from datetime import datetime
from sqlmodel import SQLModel, Field, create_engine, Session
from sqlalchemy import Column, DateTime

class Product(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    categoryId: Optional[int] = Field(default=None, nullable=True)
    brandId: Optional[int] = Field(default=None, nullable=True)
    user_id: Optional[int] = Field(default=None)
    title: str
    description: str
    price: float
    image_url: Optional[str] = Field(default=None)
    quantity: Optional[int] = Field(default=None)
    rating: Optional[float] = Field(default=None)
    created_at: Optional[datetime] = Field(default_factory=datetime.utcnow, sa_column=Column(DateTime, default=datetime.utcnow))
    updated_at: Optional[datetime] = Field(default_factory=datetime.utcnow, sa_column=Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow))
    
    class Config:
        orm_mode = True
        
