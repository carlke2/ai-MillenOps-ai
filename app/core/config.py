from pydantic_settings import BaseSettings, SettingsConfigDict
from typing import Optional

class Settings(BaseSettings):
    APP_NAME: str = "Smart Ops AI Service"
    APP_ENV: str = "development"
    APP_VERSION: str = "1.0.0"
    PORT: int = 8000
    
    # Security
    API_KEY: str = "dev-api-key-change-me"
    
    # Models
    DEFAULT_MODEL_VERSION: str = "baseline-rules-v1"
    TICKET_CLASSIFIER_MODEL_PATH: str = "app/modules/tickets/classification/models/ticket_classifier.joblib"

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")

settings = Settings()
