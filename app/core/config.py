"""
Module for application configuration using Pydantic BaseSettings.
"""

from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """
    Application settings loaded from environment variables or defaults.
    """

    app_name: str = "CRSet API"
    user_agent: str = (
        "Mozilla/5.0 (compatible; crset-bot/1.0; +https://github.com/uesleibros/crset)"
    )

    class Config:  # pylint: disable=too-few-public-methods
        """
        Pydantic configuration to specify environment file.
        """
        env_file = ".env"


# Global settings instance to be used across the app
settings = Settings()
