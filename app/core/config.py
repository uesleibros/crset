from pydantic import BaseSettings

class Settings(BaseSettings):
    app_name: str = "CRSet API"
    user_agent: str = "Mozilla/5.0 (compatible; crset-bot/1.0; +https://github.com/uesleibros/crset)"

    class Config:
        env_file = ".env"

settings = Settings()