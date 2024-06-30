from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.models import Product
from sqlalchemy.exc import SQLAlchemyError, IntegrityError
from app.db.session import get_session
from app.schemas.product import ProductCreate, ProductRead,ProductUpdate
from sqlmodel import select,Session
from app.kafka.producer import kafka_producer
from app.proto import product_pb2 , user_pb2
from typing import List

router = APIRouter()
# create 
@router.post("/", response_model=ProductRead,status_code=status.HTTP_201_CREATED)
async def create_product(product: ProductCreate, db: Session = Depends(get_session)):
    # result = await db.execute(select(Product).where(Product.title == product.title))
    # db_product = result.scalar_one_or_none()
    # if db_product:
    #     raise HTTPException(status_code=400, detail="Product already registered")
    db_product = Product(
        category_id=product.category_id,
        brand_id=product.brand_id,
        user_id=product.user_id,
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
    product_message = product_pb2.Product(
        id=db_product.id,
        category_id=db_product.category_id,
        brand_id=db_product.brand_id,
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

# detail 
@router.get("/{product_id}", response_model=ProductRead)
async def read_product(product_id: int, db: Session = Depends(get_session)):
    try:
        result =  db.execute(select(Product).where(Product.id == product_id))
        product = result.scalar_one_or_none()
        # get user detail from kafka 
        # await kafka_producer.send("user_detail_request", key=str(product.user_id).encode(), value=str(product.user_id).encode())
         # Retrieve user details using Kafka (pseudo-code)
        # user_data = await get_user_details_from_kafka(product.user_id)
        if not product:
            raise HTTPException(status_code=404, detail="Product not found")
        return product
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

    # from kafka import KafkaProducer, KafkaConsumer
# from app.proto import user_pb2  # Assuming user_pb2 contains user message schema

# async def get_user_details_from_kafka(user_id: int):
    # Kafka configuration (replace with your actual settings)
    # bootstrap_servers = ["localhost:9092"]  # List of Kafka brokers
    # user_request_topic = "user_detail_request"  # Topic for sending user detail requests
    # user_response_topic = "user_detail_response"  # Topic for receiving user detail responses

    # # Create Kafka producer
    # producer = KafkaProducer(bootstrap_servers=bootstrap_servers)

    # # Create user detail request message


    # user_request = user_pb2.UserDetailRequest(user_id=user_id)
    # request_bytes = user_request.SerializeToString()

    # # Send user detail request to Kafka
    # producer.send(user_request_topic, value=request_bytes)


    # await kafka_producer.send("user_detail_request", key=str(user_id).encode(), value=request_bytes)
    # producer.flush()  # Ensure message is sent before continuing

    # Create Kafka consumer (assuming a single consumer instance)
    # consumer = KafkaConsumer(
    #     user_response_topic,
    #     bootstrap_servers=bootstrap_servers,
    #     group_id="product_detail_consumer",  # Consumer group for identification
    #     auto_offset_reset="earliest",  # Start consuming from the beginning
    # )

    # Loop to receive user detail response (timeout can be adjusted)
    # try:
    #     for message in consumer.poll(timeout=1000):  # Wait for message for 1 second
    #         user_response = user_pb2.UserDetailResponse.FromString(message.value)
    #         if user_response.user_id == user_id:
    #             return user_response.user.dict()  # Return user data as dictionary
    #         else:
    #             # Handle potential responses for other requests (if applicable)
    #             pass
    #     raise TimeoutError("User detail response not received within timeout")
    # finally:
    #     consumer.close()  # Close consumer to avoid resource leaks


