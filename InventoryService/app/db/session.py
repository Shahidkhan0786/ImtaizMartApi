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

# @contextmanager
# def get_session():
#     """Provide a transactional scope around a series of operations."""
#     session = Session(engine)
#     try:
#         yield session
#         session.commit()
#     except Exception as e:
#         session.rollback()
#         logger.error(f"Session rollback due to exception: {e}")
#         raise
#     finally:
#         session.close()

# async session 
# SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine, class_=AsyncSession)

# @asynccontextmanager
# async def get_session():
#     async with SessionLocal() as session:
#         yield session