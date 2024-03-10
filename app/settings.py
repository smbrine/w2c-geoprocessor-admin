from dotenv import load_dotenv
from pydantic_settings import BaseSettings

load_dotenv()


class Settings(BaseSettings):
    POSTGRES_URL: str
    DEBUG: bool = False
    class Config:
        env_file = ".env"


settings = Settings()
