"""Configuration."""

from typing import Literal

from pydantic_settings import BaseSettings, SettingsConfigDict


class Config(BaseSettings):
    """Configuration."""

    model_config = SettingsConfigDict(env_file=".env", extra="allow")

    theme: str = "light"
    timeout: int = 30_000

    log_level: Literal["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"] = "INFO"


def get_config() -> Config:
    """Get config."""
    return Config()
