# import os
# from pydantic import BaseSettings

# class Settings(BaseSettings):
#     PROJECT_NAME: str = "User Service"
#     SQLALCHEMY_DATABASE_URL: str = os.getenv("DATABASE_URL", "postgresql://shahidkhan:12345@PostgresUserCont:5432/imtaiz_user_db")
#     SECRET_KEY: str = os.getenv("SECRET_KEY", "your-secret-key")
#     ALGORITHM: str = "HS256"
#     ACCESS_TOKEN_EXPIRE_MINUTES: int = 30

# settings = Settings()

from pydantic_settings import BaseSettings
from typing import Union

class Settings(BaseSettings):
    DATABASE_URL: str
    SECRET_KEY: str
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30

    class Config:
        env_file = ".env"

settings = Settings()
