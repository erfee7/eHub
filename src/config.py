# src/config.py

from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    openrouter_api_key: str
    default_image_model: str = "google/gemini-2.5-flash-image"

    class Config:
        env_file = ".env"
        extra = "ignore"

settings = Settings()