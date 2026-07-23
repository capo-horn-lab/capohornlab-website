"""Application configuration via pydantic-settings."""

from __future__ import annotations

from typing import List, Optional

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
    )

    # --- App ---
    APP_NAME: str = "Capo Horn Lab"
    APP_VERSION: str = "1.0.0"
    APP_ENV: str = "development"
    DEBUG: bool = True
    SECRET_KEY: str = "change-me-to-a-long-random-string"
    ALLOWED_ORIGINS: str = "http://localhost:5173,http://localhost:3000"

    @property
    def allowed_origins_list(self) -> List[str]:
        return [o.strip() for o in self.ALLOWED_ORIGINS.split(",") if o.strip()]

    # --- Database ---
    POSTGRES_USER: str = "capohorn"
    POSTGRES_PASSWORD: str = "capohorn_secret"
    POSTGRES_DB: str = "capohornlab"
    POSTGRES_HOST: str = "db"
    POSTGRES_PORT: int = 5432
    DATABASE_URL: Optional[str] = None
    DATABASE_URL_SYNC: Optional[str] = None

    @property
    def async_database_url(self) -> str:
        if self.DATABASE_URL:
            return self.DATABASE_URL
        return (
            f"postgresql+asyncpg://{self.POSTGRES_USER}:{self.POSTGRES_PASSWORD}"
            f"@{self.POSTGRES_HOST}:{self.POSTGRES_PORT}/{self.POSTGRES_DB}"
        )

    @property
    def sync_database_url(self) -> str:
        if self.DATABASE_URL_SYNC:
            return self.DATABASE_URL_SYNC
        return (
            f"postgresql+psycopg2://{self.POSTGRES_USER}:{self.POSTGRES_PASSWORD}"
            f"@{self.POSTGRES_HOST}:{self.POSTGRES_PORT}/{self.POSTGRES_DB}"
        )

    # --- Redis ---
    REDIS_HOST: str = "redis"
    REDIS_PORT: int = 6379
    REDIS_PASSWORD: str = "capohorn_redis"
    REDIS_DB: int = 0
    REDIS_URL: Optional[str] = None

    @property
    def redis_url(self) -> str:
        if self.REDIS_URL:
            return self.REDIS_URL
        return (
            f"redis://:{self.REDIS_PASSWORD}"
            f"@{self.REDIS_HOST}:{self.REDIS_PORT}/{self.REDIS_DB}"
        )

    # --- JWT ---
    JWT_ACCESS_SECRET: str = "change-me-access-secret"
    JWT_REFRESH_SECRET: str = "change-me-refresh-secret"
    JWT_ACCESS_EXPIRE_MINUTES: int = 15
    JWT_REFRESH_EXPIRE_DAYS: int = 7

    # --- Rate Limiting ---
    RATE_LIMIT_PER_MINUTE: int = 20

    # --- Newsletter ---
    FRONTEND_URL: str = "http://localhost:5173"
    RESEND_API_KEY: str | None = None
    NEWSLETTER_FROM_EMAIL: str = "newsletter@capohornlab.com"
    NEWSLETTER_FROM_NAME: str = "Capo Horn Lab"

    # --- File Upload ---
    UPLOAD_DIR: str = "D:\\CapoHornLab\\uploads"
    MAX_FILE_SIZE_MB: int = 10
    MAX_TOTAL_UPLOAD_MB: int = 50


settings = Settings()
