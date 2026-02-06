from pydantic_settings import BaseSettings
from typing import Optional

class Settings(BaseSettings):
    PROJECT_NAME: str = "Tavola Restaurant Management System"
    VERSION: str = "1.0.0"
    API_V1_STR: str = "/api/v1"
    SECRET_KEY: str = "your-secret-key-here"  # Change in production
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 8  # 8 days
    
    # Database
    POSTGRES_SERVER: str = "localhost"
    POSTGRES_USER: str = "postgres"
    POSTGRES_PASSWORD: str = "postgres"
    POSTGRES_DB: str = "tavola"
    DATABASE_URI: Optional[str] = None

    class Config:
        env_file = ".env"

settings = Settings()

# Update database URL if not set
if not settings.DATABASE_URI:
    # Use SQLite for development, PostgreSQL for production
    import os
    if os.getenv("USE_POSTGRES"):
        settings.DATABASE_URI = f"postgresql://{settings.POSTGRES_USER}:{settings.POSTGRES_PASSWORD}@{settings.POSTGRES_SERVER}/{settings.POSTGRES_DB}"
    else:
        # Use SQLite for development
        settings.DATABASE_URI = "sqlite:///./tavola.db"
