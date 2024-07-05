from sqlmodel import Session, create_engine
from app.core.config import settings
import logging
from contextlib import contextmanager

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

connection_string = str(settings.DATABASE_URL).replace(
    "postgresql","postgresql+psycopg2"
)

engine = create_engine(
    connection_string , connect_args={}, pool_recycle=300
)


def get_session():
    with Session(engine) as session:
        yield session
