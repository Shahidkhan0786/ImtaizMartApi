from fastapi import APIRouter, Depends, HTTPException,status
# from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import SQLAlchemyError, IntegrityError
from app.db.models import Category, Category
from app.db.session import get_session
from sqlmodel import select,Session
from app.kafka.producer import kafka_producer
from app.proto import product_pb2
from app.schemas.category import CategoryCreate, CategoryRead, CategoryUpdate,CategoryDetail
from typing import List


router = APIRouter()

@router.post("/", response_model=CategoryRead, status_code=status.HTTP_201_CREATED)
async def create_category(category: CategoryCreate, db: Session = Depends(get_session)):
    try:
        db_category = Category(
            title=category.title,
            description=category.description,
            image_url=category.image_url,
            status=category.status
        )
        db.add(db_category)
        db.commit()
        db.refresh(db_category)
        
        # Serialize a message using protobuf
        # Category_message = Category_pb2.Category(
        #     id=db_Category.id,
        #     title=db_Category.title,
        #     description=db_Category.description,
        #     image_url=db_Category.image_url,
        #     status=db_Category.status.value,
        #     created_at=db_Category.created_at.isoformat(),
        #     updated_at=db_Category.updated_at.isoformat()
        # )
        # await kafka_producer.send("Category_topic", key=str(db_Category.id).encode(), value=Category_message.SerializeToString())
        return db_category
    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Category with this title already exists")
    except SQLAlchemyError as e:
        db.rollback()
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))

@router.get("/{category_id}", response_model=CategoryDetail)
async def read_category(category_id: int, db: Session = Depends(get_session)):
    try:
        result = db.execute(select(Category).where(Category.id == category_id))
        category = result.scalar_one_or_none()
        if not category:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Category not found")
        return category
    except SQLAlchemyError as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))

@router.get("/", response_model=List[CategoryRead])
async def read_categorys(skip: int = 0, limit: int = 10, db: Session = Depends(get_session)):
    try:
        result = db.execute(select(Category).offset(skip).limit(limit))
        category = result.scalars().all()
        return category
    except SQLAlchemyError as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))

@router.put("/{category_id}", response_model=CategoryRead)
async def update_category(category_id: int, Category_update: CategoryUpdate, db: Session = Depends(get_session)):
    try:
        result = db.execute(select(Category).where(Category.id == category_id))
        category = result.scalar_one_or_none()
        if not category:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Category not found")

        category_data = Category_update.dict(exclude_unset=True)
        for key, value in category_data.items():
            setattr(category, key, value)

        db.add(category)
        db.commit()
        db.refresh(category)
        return category
    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Category with this title already exists")
    except SQLAlchemyError as e:
        db.rollback()
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))

@router.delete("/{category_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_Category(category_id: int, db: Session = Depends(get_session)):
    try:
        result = db.execute(select(Category).where(Category.id == category_id))
        category = result.scalar_one_or_none()
        if not category:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="category not found")

        db.delete(category)
        db.commit()
        return
    except SQLAlchemyError as e:
        db.rollback()
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))