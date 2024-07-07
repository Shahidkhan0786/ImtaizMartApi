from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    DATABASE_URL:str
    RETRY_TIME: float
    RETRY_COUNT: int 

    class Config:
        env_file = ".env"

settings = Settings()