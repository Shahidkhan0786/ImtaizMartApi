from typing import Optional
from datetime import datetime
from sqlmodel import SQLModel, Field, Relationship
from sqlalchemy import Column, DateTime,Enum as SQLAlchemyEnum
from app.enums.order_status_enum import OrderStatusEnum

class Order(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: Optional[int] = Field(default=None)
    order_number: int
    total_price: float
    description: Optional[str] = Field(default=None)
    status: OrderStatusEnum = Field(default=OrderStatusEnum.pending, sa_column=Column(SQLAlchemyEnum(OrderStatusEnum)))
    # products: list["Product"] = Relationship(back_populates="brand")
    created_at: Optional[datetime] = Field(default_factory=datetime.utcnow, sa_column=Column(DateTime, default=datetime.utcnow))
    updated_at: Optional[datetime] = Field(default_factory=datetime.utcnow, sa_column=Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow))
    
    class Config:
        orm_mode = True

class OrderItem(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    order_id: Optional[int] = Field(default=None, foreign_key="order.id")
    product_id: Optional[int] = Field(default=None)
    quantity: int = Field(default=0)
    unit_price: float = Field(default=0)
    total_price: float = Field(default=0)
    description: Optional[str] = Field(default=None)
    # image_url: Optional[str] = Field(default=None)
    # status: StatusEnum = Field(default=StatusEnum.activate, sa_column=Column(SQLAlchemyEnum(StatusEnum), default=StatusEnum.activate))
    # products: list["Product"] = Relationship(back_populates="brand")
    created_at: Optional[datetime] = Field(default_factory=datetime.utcnow, sa_column=Column(DateTime, default=datetime.utcnow))
    updated_at: Optional[datetime] = Field(default_factory=datetime.utcnow, sa_column=Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow))
    
    class Config:
        orm_mode = True

