from contextlib import asynccontextmanager
from typing import AsyncGenerator

from fastapi import FastAPI, HTTPException
from fastapi.responses import JSONResponse

from app.core.config import settings
from app.db import create_db_and_tables
from .api.endpoints import product,brand,category
import logging
from app.kafka.handlers import handle_user_response, handle_validate_token_responses
# Import Kafka startup and shutdown events
from app.kafka.producer import startup_event as producer_startup_event, shutdown_event as producer_shutdown_event
from app.kafka.consumer import kafka_consumer,startup_event as consumer_startup_event, shutdown_event as consumer_shutdown_event
# from app.utils.register_schemas import register_schema
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)



@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator[None, None]:
    try:
        logger.info("Creating tables...")
        create_db_and_tables()
        logger.info("Tables created successfully.")

        # logger.info("Registering schemas...")
        # with open('app/proto/product.proto', 'r') as file:
        #     product_schema = file.read()
        # with open('app/proto/user.proto', 'r') as file:
        #     user_schema = file.read()
        # register_schema(product_schema, 'product-value')
        # register_schema(user_schema, 'user-value')
        # logger.info("Schemas registered successfully.")


        
        logger.info("Starting Kafka producer...")
        await producer_startup_event()
        logger.info("Kafka producer started successfully.")
        
        logger.info("Starting Kafka consumer...")
        kafka_consumer.subscribe(["user_response_topic"], handle_user_response)
        kafka_consumer.subscribe(["validate_token_response_topic"], handle_validate_token_responses)
        await consumer_startup_event()

        logger.info("Kafka consumer started successfully.")
        
        yield
        
    except Exception as e:
        logger.error(f"Error during startup: {e}")
        raise HTTPException(status_code=500, detail=f"Internal server error: {e}")

    try:
        logger.info("Stopping Kafka producer...")
        await producer_shutdown_event()
        logger.info("Kafka producer stopped successfully.")
        
        logger.info("Stopping Kafka consumer...")
        await consumer_shutdown_event()
        logger.info("Kafka consumer stopped successfully.")
        
    except Exception as e:
        logger.error(f"Error during shutdown: {e}")


app = FastAPI(
    lifespan=lifespan,
    title="Product SERVICE API",
    version="0.0.1",
    servers=[
        #  {
        #     "url": "http://0.0.0.0:8000",  # ADD NGROK URL Here Before Creating GPT Action
        #     "description": "Development Server 1"
        # },
          {
            "url": "http://localhost:8011",  # ADD NGROK URL Here Before Creating GPT Action
            "description": "Development Server"
        }
    ]
)

# Include the brand router
app.include_router(brand.router, prefix="/product/brands", tags=["brand"])
# Include the category router
app.include_router(category.router, prefix="/product/categories", tags=["category"])
app.include_router(product.router, prefix="/product/products", tags=["product"])

@app.get("/")
def read_root():
    return {"message": "Product Service is running"}

@app.exception_handler(Exception)
async def global_exception_handler(request, exc):
    logger.error(f"Unexpected error: {exc}")
    return JSONResponse(
        status_code=500,
        content={"message": "An internal error occurred. Please try again later."},
    )
