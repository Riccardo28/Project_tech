from pydantic_settings import BaseSettings
from typing import List


class Settings(BaseSettings):
    # Project metadata
    PROJECT_NAME: str = "Project Tech API"
    VERSION: str = "1.0.0"
    DESCRIPTION: str = "A structured FastAPI project template"

    # API Configuration
    API_V1_PREFIX: str = "/api/v1"

    # CORS settings
    ALLOWED_ORIGINS: List[str] = [
        "http://localhost:3000",
        "http://localhost:5173",  # Vite default port
        "http://localhost:8000",
        "https://*.vercel.app",  # All Vercel preview deployments
        "https://project-tech-gto4pr0wy-rbellini.vercel.app",  # Current Vercel deployment
    ]

    # Security
    SECRET_KEY: str = "your-secret-key-here-change-in-production"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30

    # Database (uncomment and configure when needed)
    # DATABASE_URL: str = "sqlite:///./app.db"
    # DATABASE_URL: str = "postgresql://user:password@localhost/dbname"

    class Config:
        env_file = ".env"
        case_sensitive = True


settings = Settings()
