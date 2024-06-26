from .models import User, Profile
from sqlmodel import SQLModel
from sqlalchemy.exc import SQLAlchemyError
from fastapi import HTTPException
from app.db.session import engine
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def create_db_and_tables():
    try:
        SQLModel.metadata.create_all(engine)
        logger.info("Database and tables created successfully.")
    except SQLAlchemyError as e:
        logger.error(f"Error creating database tables: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")
