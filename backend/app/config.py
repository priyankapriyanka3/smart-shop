"""
Application configuration module.
Loads environment variables and provides application settings.
"""
import os


class Settings:
    """Application settings loaded from environment variables."""

    def __init__(self):
        """Initialize settings and validate security configuration."""
        # Database
        self.database_url: str = os.getenv("DATABASE_URL", "sqlite:///./app.db")

        # JWT
        self.jwt_secret: str = os.getenv("JWT_SECRET", "")
        self.jwt_algorithm: str = "HS256"
        self.jwt_expiration_hours: int = 24

        # Server
        self.backend_port: int = int(os.getenv("BACKEND_PORT", "8000"))

        # CORS
        self.cors_origins: str = os.getenv(
            "CORS_ORIGINS",
            "http://localhost:5173,http://localhost:3000"
        )

        # Payment Provider (mock for development)
        self.payment_provider_url: str | None = os.getenv("PAYMENT_PROVIDER_URL")
        self.payment_provider_api_key: str | None = os.getenv("PAYMENT_PROVIDER_API_KEY")

        # Validate critical security settings
        self._validate_jwt_secret()

    def _validate_jwt_secret(self):
        """Validate JWT secret is strong and secure."""
        if not self.jwt_secret:
            raise ValueError(
                "JWT_SECRET environment variable is required. "
                "Generate one with: openssl rand -base64 32"
            )
        if len(self.jwt_secret) < 32:
            raise ValueError(
                f"JWT_SECRET must be at least 32 characters long for security. "
                f"Current length: {len(self.jwt_secret)}"
            )
        # Check for known weak secrets
        weak_secrets = [
            "dev-secret-change-in-production-please",
            "dev-secret-change-in-production",
            "secret",
            "password",
            "changeme",
        ]
        if self.jwt_secret.lower() in weak_secrets:
            raise ValueError(
                "JWT_SECRET contains a known weak value. "
                "Generate a strong secret with: openssl rand -base64 32"
            )

    @property
    def cors_origins_list(self) -> list[str]:
        """Return CORS origins as a list."""
        return [origin.strip() for origin in self.cors_origins.split(",")]


settings = Settings()
