from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.models import Product
from app.db.session import get_session
from app.schemas.product import ProductCreate, ProductRead
from sqlmodel import select,Session
from app.kafka.producer import kafka_producer
from app.proto import product_pb2

router = APIRouter()

@router.post("/", response_model=ProductRead)
async def create_product(product: ProductCreate, db: Session = Depends(get_session)):
    # result = await db.execute(select(Product).where(Product.title == product.title))
    # db_product = result.scalar_one_or_none()
    # if db_product:
    #     raise HTTPException(status_code=400, detail="Product already registered")
    db_product = Product(
        # categoryId=product.categoryId,
        # brandId=product.brandId,
        # user_id=product.user_id,
        title=product.title,
        description=product.description,
        price=product.price,
        # image_url=product.image_url,
        quantity=product.quantity,
        rating=product.rating
    )
    db.add(db_product)
    db.commit()
    db.refresh(db_product)
    # Serialize a message using protobuf
    product_message = product_pb2.Product(
        id=db_product.id,
        categoryId=db_product.categoryId,
        brandId=db_product.brandId,
        user_id=db_product.user_id,
        title=db_product.title,
        description=db_product.description,
        price=db_product.price,
        image_url=db_product.image_url,
        quantity=db_product.quantity,
        rating=db_product.rating,
        created_at=db_product.created_at.isoformat(),
        updated_at=db_product.updated_at.isoformat()
    )
    await kafka_producer.send("product_topic", key=str(db_product.id).encode(), value=product_message.SerializeToString())
    return db_product

@router.get("/{product_id}", response_model=ProductRead)
async def read_product(product_id: int, db: AsyncSession = Depends(get_session)):
    result = await db.execute(select(Product).where(Product.id == product_id))
    product = result.scalar_one_or_none()
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    return product
