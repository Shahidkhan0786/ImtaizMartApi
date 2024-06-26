from sqlmodel import SQLModel,Field
from sqlalchemy import Column,Enum as SQLAlchemyEnum,String
from app.enums.status_enum import StatusEnum

class User(SQLModel, table=True):
    id: int|None = Field(default=None , primary_key=True)
    first_name: str
    last_name: str | None = None
    email: str
    password: str
    status: StatusEnum = Field(default=StatusEnum.active,sa_column=Column(SQLAlchemyEnum(StatusEnum)))

    class Config:
        orm_mode = True
    
class Profile(SQLModel , table=True):
    id: int | None = Field(default=None , primary_key=True)
    user_id: int = Field(foreign_key="user.id")
    city: str | None = None
    phone: str | None = None
    address: str | None = Field(default=None, sa_column=Column(String(255)))
    
    class Config:
        orm_mode = True
        


