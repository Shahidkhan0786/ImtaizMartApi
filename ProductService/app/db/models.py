from typing import Optional
from datetime import datetime
from sqlmodel import SQLModel, Field, create_engine, Session,Relationship
from sqlalchemy import Column, DateTime,Enum as SQLAlchemyEnum
from app.enums.status_enum import StatusEnum

class Brand(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    title: str
    description: Optional[str] = Field(default=None)
    image_url: Optional[str] = Field(default=None)
    status: StatusEnum = Field(default=StatusEnum.activate, sa_column=Column(SQLAlchemyEnum(StatusEnum), default=StatusEnum.activate))
    products: list["Product"] = Relationship(back_populates="brand")
    created_at: Optional[datetime] = Field(default_factory=datetime.utcnow, sa_column=Column(DateTime, default=datetime.utcnow))
    updated_at: Optional[datetime] = Field(default_factory=datetime.utcnow, sa_column=Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow))
    
    class Config:
        orm_mode = True

class Category(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    title: str
    description: Optional[str] = Field(default=None)
    image_url: Optional[str] = Field(default=None)
    status: StatusEnum = Field(default=StatusEnum.activate, sa_column=Column(SQLAlchemyEnum(StatusEnum), default=StatusEnum.activate))
    products: list["Product"] = Relationship(back_populates="category")
    created_at: Optional[datetime] = Field(default_factory=datetime.utcnow, sa_column=Column(DateTime, default=datetime.utcnow))
    updated_at: Optional[datetime] = Field(default_factory=datetime.utcnow, sa_column=Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow))
    
    class Config:
        orm_mode = True


class Product(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    category_id: Optional[int] = Field(default=None, foreign_key="category.id")
    # category_id: Optional[int] = Field(default=None, nullable=True)
    brand_id: Optional[int]= Field(default=None, foreign_key="brand.id")
    # brand_id: Optional[int] = Field(default=None, nullable=True)
    # user_id: Optional[int] = Field(default=None, forigen_key="user.id")
    user_id: Optional[int] = Field(default=None)
    title: str
    description: str
    price: float
    image_url: Optional[str] = Field(default=None)
    quantity: Optional[int] = Field(default=None)
    rating: Optional[float] = Field(default=None)
    status: StatusEnum = Field(default=StatusEnum.activate, sa_column=Column(SQLAlchemyEnum(StatusEnum), default=StatusEnum.activate))
    created_at: Optional[datetime] = Field(default_factory=datetime.utcnow, sa_column=Column(DateTime, default=datetime.utcnow))
    updated_at: Optional[datetime] = Field(default_factory=datetime.utcnow, sa_column=Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow))
    brand: Optional[Brand] = Relationship(back_populates="products")
    category: Optional[Category] = Relationship(back_populates="products")
    class Config:
        orm_mode = True
        

