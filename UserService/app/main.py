from contextlib import asynccontextmanager
from typing import AsyncGenerator

from fastapi import FastAPI, HTTPException
from fastapi.responses import JSONResponse

from app.core.config import settings
from app.db import create_db_and_tables
from .api.endpoints import auth,user
import logging

# Import Kafka startup and shutdown events
from app.kafka.producer import startup_event as producer_startup_event, shutdown_event as producer_shutdown_event
from app.kafka.consumer import  kafka_consumer, startup_event as consumer_startup_event, shutdown_event as consumer_shutdown_event
from app.kafka.handlers import handle_user_request


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)



@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator[None, None]:
    try:
        logger.info("Creating tables...")
        create_db_and_tables()
        logger.info("Tables created successfully.")
        
        logger.info("Starting Kafka producer...")
        await producer_startup_event()
        logger.info("Kafka producer started successfully.")
        
        logger.info("Starting Kafka consumer...")
        kafka_consumer.subscribe(["user_request_topic"], handle_user_request)
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
    title="USER SERVICE API",
    version="0.0.1",
    servers=[
          {
            "url": "http://localhost:8010",  # ADD NGROK URL Here Before Creating GPT Action
            "description": "Development Server"
            }
    ]
)

# Include the auth router
app.include_router(auth.router, prefix="/auth", tags=["auth"])
app.include_router(user.router, prefix="/user", tags=["user"])


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
