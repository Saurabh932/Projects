'''
    This file reads the environment variable
'''

from pydantic_settings import BaseSettings, SettingsConfigDict

class Setting(BaseSettings):
    DATABASE_URL : str
    JWT_SECRET : str
    JWT_ALGORITHM : str
    ADMIN_EMAIL: str
    ADMIN_PASSWORD: str
    
    model_config = SettingsConfigDict(
        env_file="src/.env",
        extra="ignore"
    )
    
config = Setting()