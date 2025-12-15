from pydantic_settings import BaseSettings
from typing import List

class Settings(BaseSettings):
    APP_NAME: str = "ReachCraft"
    APP_ENV: str = "development"
    DEBUG: bool = True
    
    # We'll add more config later as needed
    
    class Config:
        env_file = ".env"

settings = Settings()