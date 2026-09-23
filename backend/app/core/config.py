from functools import lru_cache

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    app_name: str = "WorkForceIQ"
    environment: str = "development"
    database_url: str = "sqlite:///./workforceiq.db"
    jwt_secret: str = "dev-only-change-me"
    jwt_algorithm: str = "HS256"
    access_token_expire_minutes: int = 60
    backend_cors_origins: str = Field(
        default="http://localhost:3000,http://127.0.0.1:3000"
    )
    redis_url: str = "redis://localhost:6379/0"
    llm_api_key: str | None = None
    embedding_api_key: str | None = None

    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    @property
    def cors_origins(self) -> list[str]:
        return [origin.strip() for origin in self.backend_cors_origins.split(",") if origin.strip()]


@lru_cache
def get_settings() -> Settings:
    return Settings()


settings = get_settings()

