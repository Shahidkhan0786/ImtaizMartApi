from fastapi import APIRouter, Depends, HTTPException,status
# from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import SQLAlchemyError, IntegrityError
from app.db.models import Brand , Order , OrderItem
from app.db.session import get_session
from sqlmodel import select,Session
from app.kafka.producer import kafka_producer
from app.proto import product_pb2
from app.schemas.brand import BrandCreate, BrandRead, BrandUpdate,BrandDetail
from app.schemas.order import OrderCreate , OrderRead
from typing import List


router = APIRouter()

@router.post("/", response_model=BrandRead, status_code=status.HTTP_201_CREATED)
async def create_order(order: OrderCreate, db: Session = Depends(get_session)):
    try:
        db_order = Order(
            title=order.title,
            description=order.description,
            image_url=order.image_url,
            status=order.status
        )
        db.add(db_order)
        db.commit()
        db.refresh(db_order)
        
        # Serialize a message using protobuf
        # brand_message = brand_pb2.Brand(
        #     id=db_brand.id,
        #     title=db_brand.title,
        #     description=db_brand.description,
        #     image_url=db_brand.image_url,
        #     status=db_brand.status.value,
        #     created_at=db_brand.created_at.isoformat(),
        #     updated_at=db_brand.updated_at.isoformat()
        # )
        # await kafka_producer.send("brand_topic", key=str(db_brand.id).encode(), value=brand_message.SerializeToString())
        return db_order
    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Order with this title already exists")
    except SQLAlchemyError as e:
        db.rollback()
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))

@router.get("/{brand_id}", response_model=BrandDetail)
async def read_brand(brand_id: int, db: Session = Depends(get_session)):
    try:
        result = db.execute(select(Brand).where(Brand.id == brand_id))
        brand = result.scalar_one_or_none()
        if not brand:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Brand not found")
        return brand
    except SQLAlchemyError as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))

@router.get("/", response_model=List[BrandRead])
async def read_brands(skip: int = 0, limit: int = 10, db: Session = Depends(get_session)):
    try:
        result = db.execute(select(Brand).offset(skip).limit(limit))
        brands = result.scalars().all()
        return brands
    except SQLAlchemyError as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))

@router.put("/{brand_id}", response_model=BrandRead)
async def update_brand(brand_id: int, brand_update: BrandUpdate, db: Session = Depends(get_session)):
    try:
        result = db.execute(select(Brand).where(Brand.id == brand_id))
        brand = result.scalar_one_or_none()
        if not brand:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Brand not found")

        brand_data = brand_update.dict(exclude_unset=True)
        for key, value in brand_data.items():
            setattr(brand, key, value)

        db.add(brand)
        db.commit()
        db.refresh(brand)
        return brand
    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Brand with this title already exists")
    except SQLAlchemyError as e:
        db.rollback()
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))

@router.delete("/{brand_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_brand(brand_id: int, db: Session = Depends(get_session)):
    try:
        result = db.execute(select(Brand).where(Brand.id == brand_id))
        brand = result.scalar_one_or_none()
        if not brand:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Brand not found")

        db.delete(brand)
        db.commit()
        return
    except SQLAlchemyError as e:
        db.rollback()
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))