from fastapi import APIRouter, Depends, HTTPException, status , Header
import asyncio
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.models import Product
from sqlalchemy.exc import SQLAlchemyError, IntegrityError
from app.db.session import get_session
from app.schemas.product import ProductCreate, ProductRead,ProductUpdate,ProductDetail
from app.schemas.auth import TokenResponse
from sqlmodel import select,Session
from app.kafka.producer import kafka_producer
from app.proto import product_pb2 , user_pb2
from typing import List , Optional  , Annotated , Union
from app.api.deps import decode_validate_token
from app.kafka.handlers import user_info_store
router = APIRouter()


# create 
@router.post("/", response_model=ProductRead,status_code=status.HTTP_201_CREATED)
async def create_product(product: ProductCreate, db: Session = Depends(get_session) , current_user:Annotated[Union[TokenResponse , None] , Depends(decode_validate_token)]= None):
    
    # result = await db.execute(select(Product).where(Product.title == product.title))
    # db_product = result.scalar_one_or_none()
    # if db_product:
    #     raise HTTPException(status_code=400, detail="Product already registered")
    print(current_user)
    db_product = Product(
        category_id=product.category_id,
        brand_id=product.brand_id,
        user_id=current_user["id"], 
        title=product.title,
        description=product.description,
        price=product.price,
        image_url=product.image_url,
        quantity=product.quantity,
        rating=product.rating
    )
    db.add(db_product)
    db.commit()
    db.refresh(db_product)
    # Serialize a message using protobuf
    # for testing purposes 
    # product_message = product_pb2.Product(
    #     id=db_product.id,
    #     category_id=db_product.category_id,
    #     brand_id=db_product.brand_id,
    #     user_id=db_product.user_id,
    #     title=db_product.title,
    #     description=db_product.description,
    #     price=db_product.price,
    #     image_url=db_product.image_url,
    #     quantity=db_product.quantity,
    #     rating=db_product.rating,
    #     created_at=db_product.created_at.isoformat(),
    #     updated_at=db_product.updated_at.isoformat()
    # )
    # await kafka_producer.send("product_topic", key=str(db_product.id).encode(), value=product_message.SerializeToString())
    return db_product

# detail 
@router.get("/{product_id}", response_model=ProductDetail)
async def read_product(product_id: int, db: Session = Depends(get_session)):
    try:
        result =  db.execute(select(Product).where(Product.id == product_id))
        product = result.scalar_one_or_none()
        if not product:
            raise HTTPException(status_code=404, detail="Product not found")
        # Fetch user information
        user_info = await fetch_user_info(product.user_id)
        if not user_info:
            raise HTTPException(status_code=404, detail="User not found")

        print("Inn Endpoint", user_info)
        return {
            **product.dict(),
            "owner": user_info
        }
    except SQLAlchemyError as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))
    

# list 
@router.get("/", response_model=List[ProductRead])
async def list_products(skip: int = 0, limit: int = 10, db: Session = Depends(get_session)):
    try:
        result = db.execute(select(Product).offset(skip).limit(limit))
        product = result.scalars().all()
        return product
    except SQLAlchemyError as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))


# update
@router.put("/{category_id}", response_model=ProductRead)
async def update_product(product_id: int, product_update: ProductUpdate, db: Session = Depends(get_session)):
    try:
        result = db.execute(select(Product).where(Product.id == product_id))
        product = result.scalar_one_or_none()
        if not product:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="product not found")

        product_data = product_update.dict(exclude_unset=True)
        for key, value in product_data.items():
            setattr(product, key, value)

        db.add(product)
        db.commit()
        db.refresh(product)
        return product
    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="product with this title already exists")
    except SQLAlchemyError as e:
        db.rollback()
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))

# del 
@router.delete("/{product_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_poduct(product_id: int, db: Session = Depends(get_session)):
    try:
        result = db.execute(select(Product).where(Product.id == product_id))
        product = result.scalar_one_or_none()
        if not product:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="product not found")

        db.delete(product)
        db.commit()
        return
    except SQLAlchemyError as e:
        db.rollback()
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))
    

# kafka 


async def validate_token(token: str) -> bool:
   
    if not token or not token.startswith("Bearer "):
        raise HTTPException(status_code=403, detail="Token is missing or invalid")
    
    # Create a Kafka message to validate the token
    token_message = {"token": token}
    await kafka_producer.send("validate_token_topic", value=token_message)
    
    # Wait for user info to be available in user_info_store
    # for _ in range(10):  # Retry 10 times with a delay
    #     if user_id in user_info_store:
    #         return user_info_store.pop(user_id)
    #     await asyncio.sleep(0.5)  # Wait for 0.5 second before retrying

    # raise HTTPException(status_code=404, detail="User not found")

    # Check if the token is valid
    # This is a placeholder for actual validation logic
    return True  # Assume token is valid for now

    
# Function to fetch user info via Kafka
async def fetch_user_info(user_id: int) -> Optional[dict]:
    request_message = user_pb2.UserDetailRequest(user_id=user_id)
    await kafka_producer.send("user_request_topic", key=str(user_id).encode(), value=request_message.SerializeToString())

    # Wait for user info to be available in user_info_store
    for _ in range(10):  # Retry 10 times with a delay
        if user_id in user_info_store:
            return user_info_store.pop(user_id)
        await asyncio.sleep(0.5)  # Wait for 0.5 second before retrying

    raise HTTPException(status_code=404, detail="User not found")

