# main.py
from contextlib import asynccontextmanager
from typing import Union, Optional, Annotated
from app import settings
from sqlmodel import Field, Session, SQLModel, create_engine
from fastapi import FastAPI, Depends
from pydantic import BaseModel, EmailStr
from typing import AsyncGenerator

class Product(SQLModel, table=False):
    id: Optional[int] = Field(default=None, primary_key=True)
    first_name: str = Field()
    last_name: str = Field()
    email: str = Field(unique=True, index=True)
    # Add password field securely (not shown for security reasons)
    password: str = Field(default=None)  # Placeholder, replace with secure hashing
    phone_number: Optional[str] = Field(default=None)


# only needed for psycopg 3 - replace postgresql
# with postgresql+psycopg in settings.DATABASE_URL
connection_string = str(settings.DATABASE_URL).replace(
    "postgresql", "postgresql+psycopg"
)


# recycle connections after 5 minutes
# to correspond with the compute scale down
engine = create_engine(
    connection_string, connect_args={}, pool_recycle=300
)

#engine = create_engine(
#    connection_string, connect_args={"sslmode": "require"}, pool_recycle=300
#)


def create_db_and_tables()->None:
    SQLModel.metadata.create_all(engine)




# The first part of the function, before the yield, will
# be executed before the application starts.
# https://fastapi.tiangolo.com/advanced/events/#lifespan-function
# loop = asyncio.get_event_loop()
@asynccontextmanager
async def lifespan(app: FastAPI)-> AsyncGenerator[None, None]:
    print("Creating tables..")
    # task = asyncio.create_task(consume_messages('todos', 'broker:19092'))
    # create_db_and_tables()
    yield


app = FastAPI(lifespan=lifespan, title="PRODUCT SERVICE API", 
    version="0.0.1",
    servers=[
        {
            "url": "http://127.0.0.1:8000", # ADD NGROK URL Here Before Creating GPT Action
            "description": "Development Server"
        }
        ])

def get_session():
    with Session(engine) as session:
        yield session


@app.get("/")
def read_root():
    return {"Hello": "product Services"}

