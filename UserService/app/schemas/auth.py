from pydantic import BaseModel
from app.enums.status_enum import StatusEnum
from typing import List
# class UserCreate(BaseModel):
#     first_name: str
#     last_name: str | None = None
#     email: str
#     password: str

# class UserRead(BaseModel):
#     id: int
#     first_name: str
#     last_name: str | None = None
#     email: str
#     status: StatusEnum

#     class Config:
#         orm_mode = True

# class ProfileCreate(BaseModel):
#     user_id: int
#     city: str | None = None
#     phone: str | None = None
#     address: str | None = None
#     image_url: str | None = None

# class ProfileRead(BaseModel):
#     id: int
#     user_id: int
#     city: str | None = None
#     phone: str | None = None
#     address: str | None = None

#     class Config:
#         orm_mode = True

class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"
    # refresh_token: str | None = None
    # expires_in: int

class TokenData(Token):
    first_name: str| None
    email: str
    # roles: List[str] = []

