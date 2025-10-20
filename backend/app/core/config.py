from pydantic_settings import BaseSettings
from typing import List
import os


class Settings(BaseSettings):
    # Project metadata
    PROJECT_NAME: str = "Project Tech API"
    VERSION: str = "1.0.0"
    DESCRIPTION: str = "A structured FastAPI project template"

    # API Configuration
    API_V1_PREFIX: str = "/api/v1"

    # CORS settings
    # Note: Safari/iOS don't support wildcard origins, so we list them explicitly
    # Can be overridden via ALLOWED_ORIGINS environment variable (comma-separated)
    ALLOWED_ORIGINS: List[str] = [
        "http://localhost:3000",
        "http://localhost:5173",  # Vite default port
        "http://localhost:8000",
        "https://project-tech-chi.vercel.app",  # Production deployment
        "https://project-tech-gto4pr0wy-rbellini.vercel.app",  # Preview deployment
    ]

    @property
    def cors_origins(self) -> List[str]:
        """Get CORS origins, supporting environment variable override"""
        env_origins = os.getenv("ALLOWED_ORIGINS")
        if env_origins:
            return [origin.strip() for origin in env_origins.split(",")]
        return self.ALLOWED_ORIGINS

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
