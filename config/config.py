import os
from functools import lru_cache
from typing import Optional

from pydantic_settings import BaseSettings, SettingsConfigDict

_env = os.getenv("APP_ENV", "debug").lower()
_env_files = [".env", f".env.{_env}"]


class Settings(BaseSettings):
    TITLE: Optional[str] = None

    HOST: Optional[str] = None
    PORT: Optional[int] = None
    VERSION: Optional[str] = None
    DEBUG: bool = None

    REDIS_URL: Optional[str] = None
    MIN_POOL_SIZE: Optional[int] = None
    MAX_POOL_SIZE: Optional[int] = None
    TIMEOUT: Optional[int] = None
    DECODE_RESPONSES: Optional[bool] = None
    ENCODING: Optional[str] = None
    SSL: Optional[bool] = None
    REDIS_DB : Optional[int] = None

    SECRET_KEY: Optional[str] = None
    ALGORITHM: Optional[str] = None
    ACCESS_TOKEN_EXPIRE_MINUTES: Optional[int] = None
    REFRESH_TOKEN_EXPIRE_DAYS: Optional[int] = None

    ASYNC_DATABASE_URI: Optional[str] = None

    model_config = SettingsConfigDict(
        env_file=_env_files, env_file_encoding="utf-8", extra="allow"
    )


@lru_cache
def get_settings() -> Settings:
    return Settings()


settings = get_settings()
