from fastapi import APIRouter, Depends, HTTPException , status
from sqlalchemy.exc import SQLAlchemyError, IntegrityError
from sqlmodel import Session, select
from app.db.session import get_session
from app.db.models import  Inventory
from app.schemas.inventory import InventoryRead,InventoryCreate ,InventoryDetail,InventoryUpdate
from app.schemas.auth import TokenResponse
from app.enums.status_enum import StatusEnum
from app.api.deps import role_check
from typing import Annotated , Union

router = APIRouter()


# Create
@router.post("/", response_model=InventoryRead, status_code=status.HTTP_201_CREATED)
async def create_inventory(inventory: InventoryCreate, db: Session = Depends(get_session), current_user: Annotated[Union[TokenResponse, None], Depends(role_check(['admin']))] = None):
    print(current_user)
    db_inventory = Inventory(
        product_id=inventory.product_id,
        title=inventory.title,
        quantity=inventory.quantity,
        description=inventory.description,
        transaction_type=inventory.transaction_type,
        updated_by=current_user["id"],
        details=inventory.details,
    )
    db.add(db_inventory)
    db.commit()
    db.refresh(db_inventory)
    return db_inventory

# Detail
@router.get("/{inventory_id}", response_model=InventoryDetail)
async def read_inventory(inventory_id: int, db: Session = Depends(get_session)):
    try:
        result = db.execute(select(Inventory).where(Inventory.id == inventory_id))
        inventory = result.scalar_one_or_none()
        if not inventory:
            raise HTTPException(status_code=404, detail="Inventory not found")
        return inventory
    except SQLAlchemyError as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))

# List
@router.get("/", response_model=list[InventoryRead])
async def list_inventory(skip: int = 0, limit: int = 10, db: Session = Depends(get_session)):
    try:
        result = db.execute(select(Inventory).offset(skip).limit(limit))
        inventory = result.scalars().all()
        return inventory
    except SQLAlchemyError as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))

# Update
@router.put("/{inventory_id}", response_model=InventoryRead)
async def update_inventory(inventory_id: int, inventory_update: InventoryUpdate, db: Session = Depends(get_session), current_user: Annotated[Union[TokenResponse, None], Depends(role_check(['admin']))] = None):
    try:
        result = db.execute(select(Inventory).where(Inventory.id == inventory_id))
        inventory = result.scalar_one_or_none()
        if not inventory:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Inventory not found")

        inventory_data = inventory_update.dict(exclude_unset=True)
        for key, value in inventory_data.items():
            setattr(inventory, key, value)

        db.add(inventory)
        db.commit()
        db.refresh(inventory)
        return inventory
    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Inventory with this title already exists")
    except SQLAlchemyError as e:
        db.rollback()
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))

# Delete
@router.delete("/{inventory_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_inventory(inventory_id: int, db: Session = Depends(get_session), current_user: Annotated[Union[TokenResponse, None], Depends(role_check(['admin']))] = None):
    try:
        result = db.execute(select(Inventory).where(Inventory.id == inventory_id))
        inventory = result.scalar_one_or_none()
        if not inventory:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Inventory not found")

        db.delete(inventory)
        db.commit()
    except SQLAlchemyError as e:
        db.rollback()
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))