from typing import Optional
from datetime import datetime
from sqlmodel import SQLModel, Field,Relationship
from sqlalchemy import Column, DateTime,Enum as SQLAlchemyEnum
from app.enums.status_enum import StatusEnum

class User(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    first_name: str
    last_name: Optional[str] = Field(default=None)
    email: str
    password: str
    status: StatusEnum = Field(default=StatusEnum.activate, sa_column=Column(SQLAlchemyEnum(StatusEnum), default=StatusEnum.activate))
    profile: "Profile" = Relationship(back_populates="user")
    created_at: Optional[datetime] = Field(default_factory=datetime.utcnow, sa_column=Column(DateTime, default=datetime.utcnow))
    updated_at: Optional[datetime] = Field(default_factory=datetime.utcnow, sa_column=Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow))
    
    class Config:
        orm_mode = True


class Profile(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: Optional[int]= Field(default=None, foreign_key="user.id")
    city: str| None = None
    phone: str| None = None
    address: str| None = None
    image_url: str| None = None
    owner: "Profile" = Relationship(back_populates="profile")
    created_at: Optional[datetime] = Field(default_factory=datetime.utcnow, sa_column=Column(DateTime, default=datetime.utcnow))
    updated_at: Optional[datetime] = Field(default_factory=datetime.utcnow, sa_column=Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow))
    
    class Config:
        orm_mode = True