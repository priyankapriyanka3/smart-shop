"""
Application configuration module.
Loads environment variables and provides application settings.
"""
import os
from typing import Optional


class Settings:
    """Application settings loaded from environment variables."""
    
    # Database
    database_url: str = os.getenv("DATABASE_URL", "sqlite:///./app.db")
    
    # JWT
    jwt_secret: str = os.getenv("JWT_SECRET", "dev-secret-change-in-production-please")
    jwt_algorithm: str = "HS256"
    jwt_expiration_hours: int = 24
    
    # Server
    backend_port: int = int(os.getenv("BACKEND_PORT", "8000"))
    
    # CORS
    cors_origins: str = os.getenv(
        "CORS_ORIGINS",
        "http://localhost:5173,http://localhost:3000"
    )
    
    @property
    def cors_origins_list(self) -> list[str]:
        """Return CORS origins as a list."""
        return [origin.strip() for origin in self.cors_origins.split(",")]
    
    # Payment Provider (mock for development)
    payment_provider_url: Optional[str] = os.getenv("PAYMENT_PROVIDER_URL")
    payment_provider_api_key: Optional[str] = os.getenv("PAYMENT_PROVIDER_API_KEY")


settings = Settings()
