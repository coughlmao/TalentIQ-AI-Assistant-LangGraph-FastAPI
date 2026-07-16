# app/config.py

from functools import lru_cache

from pydantic import AnyHttpUrl, Field, computed_field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        extra="ignore",
    )

    GOOGLE_API_KEY: str | None = None
    CLIENT_URL: AnyHttpUrl = "http://localhost:5173"  # type: ignore
    EXPRESS_API_URL: str = "http://localhost:3000/api"
    
    # 1. Pydantic reads the string from your .env under "INTERNAL_SHARED_SECRET"
    # No leading underscore here, so Pydantic is perfectly happy.
    internal_shared_secret_str: str = Field(
        default="fallback_secure_key",
        validation_alias="INTERNAL_SHARED_SECRET",
    )

    # 2. Expose it precisely how you want it consumed globally
    @computed_field  # Makes it visible as a property on the model
    @property
    def INTERNAL_SHARED_SECRET(self) -> bytes:  # noqa: N802
        return self.internal_shared_secret_str.encode("utf-8")


@lru_cache
def get_settings() -> Settings:
    return Settings()


settings = get_settings()
