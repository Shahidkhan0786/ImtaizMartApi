from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    DATABASE_URL:str
    RETRY_TIME: float
    RETRY_COUNT: int 
    STRIPE_SECRET_KEY:str

    class Config:
        env_file = ".env"

settings = Settings()