from sqlmodel import SQLModel,Field , Relationship
from sqlalchemy import Column,DateTime,Enum as SQLAlchemyEnum,String
from datetime import datetime
from typing import Optional
from app.enums.status_enum import StatusEnum
from app.enums.user_type_enum import UserType

class User(SQLModel, table=True):
    id: int|None = Field(default=None , primary_key=True)
    first_name: str
    last_name: str | None = None
    email: str
    password: str
    user_type: Optional[UserType] = Field(default=UserType.customer,sa_column=Column(SQLAlchemyEnum(UserType)))
    status: StatusEnum = Field(default=StatusEnum.active,sa_column=Column(SQLAlchemyEnum(StatusEnum)))
    profile: Optional["Profile"] = Relationship(back_populates="user")
    created_at: Optional[datetime] = Field(default_factory=datetime.utcnow, sa_column=Column(DateTime, default=datetime.utcnow))
    updated_at: Optional[datetime] = Field(default_factory=datetime.utcnow, sa_column=Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow))
    class Config:
        orm_mode = True
    
class Profile(SQLModel , table=True):
    id: int | None = Field(default=None , primary_key=True)
    user_id: int = Field(foreign_key="user.id")
    city: str | None = None
    phone: str | None = None
    address: str | None = Field(default=None, sa_column=Column(String(255)))
    user: Optional[User] = Relationship(back_populates="profile")
    created_at: Optional[datetime] = Field(default_factory=datetime.utcnow, sa_column=Column(DateTime, default=datetime.utcnow))
    updated_at: Optional[datetime] = Field(default_factory=datetime.utcnow, sa_column=Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow))
    class Config:
        orm_mode = True
        

# class ShippingAddress(SQLModel , table=True):
#     id: int | None = Field(default=None , primary_key=True)
#     user_id: int = Field(foreign_key="user.id")
#     country: str | None = None
#     state: str | None = None
#     zip_code: str | None = None
#     city: str | None = None
#     address: str | None = Field(default=None, sa_column=Column(String(255)))
#     # user: Optional[User] = Relationship(back_populates="profile")
#     created_at: Optional[datetime] = Field(default_factory=datetime.utcnow, sa_column=Column(DateTime, default=datetime.utcnow))
#     updated_at: Optional[datetime] = Field(default_factory=datetime.utcnow, sa_column=Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow))
#     class Config:
#         orm_mode = True
