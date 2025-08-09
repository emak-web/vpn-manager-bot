from pydantic_settings import BaseSettings
from pydantic import SecretStr, Field


class Settings(BaseSettings):
    bot_token: SecretStr = Field(env='BOT_TOKEN')
    admins: list = Field(env='ADMINS')
    
    class Config:
        env_file = '.env'
        env_file_encoding = 'utf-8'
