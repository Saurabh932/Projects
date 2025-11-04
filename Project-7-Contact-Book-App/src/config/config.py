"""
This file reads environment variable.
from the .env file using pydantic-setting
"""

from pydantic_settings import BaseSettings, SettingsConfigDict

class Setting(BaseSettings):
    DATABASE_URL : str    # The PostgreSQL connecting string
    
    # configuration to specify where the .env file is located
    model_config = SettingsConfigDict(
        env_file = "src/.env",
        extra="ignore"
    )
    

# Creating a single config instance to import anywehere
config = Setting()
