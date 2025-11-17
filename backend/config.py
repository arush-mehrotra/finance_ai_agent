"""Configuration settings for the Finance AI Agent."""
from pydantic_settings import BaseSettings, SettingsConfigDict
from functools import lru_cache


class Settings(BaseSettings):
    """Application settings."""

    model_config = SettingsConfigDict(
        env_file=".env",
        case_sensitive=False,
        extra="ignore"
    )

    # API Keys
    anthropic_api_key: str
    finnhub_api_key: str

    # Server Configuration
    host: str = "0.0.0.0"
    port: int = 8000

    # AI Model Configuration
    ai_model: str = "claude-sonnet-4-5-20250929"
    ai_temperature: float = 0.7
    ai_max_tokens: int = 2048


@lru_cache()
def get_settings() -> Settings:
    """Get cached settings instance."""
    return Settings()
