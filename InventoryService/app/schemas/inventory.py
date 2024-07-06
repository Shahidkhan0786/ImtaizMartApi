from typing import Optional
from datetime import datetime
from pydantic import BaseModel
from sqlmodel import SQLModel, Field
from enum import Enum

class TransactionTypeEnum(str, Enum):
    IN = "IN"
    OUT = "OUT"

class InventoryBase(SQLModel):
    product_id: int
    title: Optional[str]
    quantity: int
    description: Optional[str]
    transaction_type: TransactionTypeEnum
    details: str

class InventoryCreate(InventoryBase):
    pass

class InventoryRead(InventoryBase):
    id: int
    updated_by: Optional[int]
    created_at: datetime

    class Config:
        orm_mode = True

class InventoryDetail(InventoryRead):
    pass

class InventoryUpdate(SQLModel):
    product_id: Optional[int]
    title: Optional[str]
    quantity: Optional[int]
    description: Optional[str]
    transaction_type: Optional[TransactionTypeEnum]
    details: Optional[str]

# class Inventory(SQLModel, table=True):
#     id: Optional[int] = Field(default=None, primary_key=True)
#     product_id: int = Field(default=None)
#     title: Optional[str] = Field(default=None)
#     quantity: int = Field(default=0)
#     description: Optional[str] = Field(default=None)
#     transaction_type: TransactionTypeEnum = Field(default=TransactionTypeEnum.IN, sa_column=Column(SQLAlchemyEnum(TransactionTypeEnum)))
#     updated_by: Optional[int] = Field(default=None)  # User who made the update
#     details: str  # Reason for the update
#     created_at: datetime = Field(default_factory=datetime.utcnow)

#     class Config:
#         orm_mode = True
