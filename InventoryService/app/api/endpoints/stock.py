from fastapi import APIRouter, HTTPException, Depends, status
from typing import List, Optional, Union, Annotated
from sqlalchemy.exc import SQLAlchemyError, IntegrityError
from sqlmodel import Session ,select
from app.db.models import Stock
from app.schemas.stock import  StockCreate, StockRead, StockUpdate
from app.db.session import get_session
from app.api.deps import role_check
from app.schemas.auth import TokenResponse
import logging

router = APIRouter()

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Create
@router.post("/", response_model=StockRead, status_code=status.HTTP_201_CREATED)
async def create_stock(stock: StockCreate, db: Session = Depends(get_session), current_user: Annotated[Union[TokenResponse, None], Depends(role_check(['admin']))] = None):
    print(current_user)
    db_stock = Stock(
        product_id=stock.product_id,
        quantity=stock.quantity,
        low_stock_threshold=stock.low_stock_threshold
    )
    db.add(db_stock)
    db.commit()
    db.refresh(db_stock)
    return db_stock

# Detail
@router.get("/{stock_id}", response_model=StockRead)
async def read_stock(stock_id: int, db: Session = Depends(get_session)):
    try:
        result = db.execute(select(Stock).where(Stock.id == stock_id))
        stock = result.scalar_one_or_none()
        if not stock:
            raise HTTPException(status_code=404, detail="Stock not found")
        return stock
    except SQLAlchemyError as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))

# List
@router.get("/", response_model=List[StockRead])
async def list_stock(skip: int = 0, limit: int = 10, db: Session = Depends(get_session)):
    try:
        result = db.execute(select(Stock).offset(skip).limit(limit))
        stock_levels = result.scalars().all()
        return stock_levels
    except SQLAlchemyError as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))

# Update
@router.put("/{stock_id}", response_model=StockRead)
async def update_stock(stock_id: int, stock_update: StockUpdate, db: Session = Depends(get_session), current_user: Annotated[Union[TokenResponse, None], Depends(role_check(['admin']))] = None):
    try:
        result = db.execute(select(Stock).where(Stock.id == stock_id))
        stock = result.scalar_one_or_none()
        if not stock:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Stock not found")

        stock_data = stock_update.dict(exclude_unset=True)
        for key, value in stock_data.items():
            setattr(stock, key, value)

        db.add(stock)
        db.commit()
        db.refresh(stock)
        return stock
    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Stock update failed")
    except SQLAlchemyError as e:
        db.rollback()
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))

# Delete
@router.delete("/{stock_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_stock(stock_id: int, db: Session = Depends(get_session), current_user: Annotated[Union[TokenResponse, None], Depends(role_check(['admin']))] = None):
    try:
        result = db.execute(select(Stock).where(Stock.id == stock_id))
        stock = result.scalar_one_or_none()
        if not stock:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Stock not found")

        db.delete(stock)
        db.commit()
    except SQLAlchemyError as e:
        db.rollback()
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))
