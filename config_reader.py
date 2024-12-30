from pydantic_settings import BaseSettings
from pydantic import SecretStr, Field


class Settings(BaseSettings):
    bot_token: SecretStr = Field(env='BOT_TOKEN')
    admins: list = Field(env='ADMINS')
    sample_config_path: str = Field(env='SAMPLE_CONFIG_PATH')
    wg_restart: str = Field(env='WG_RESTART')
    wg_status: str = Field(env='WG_STATUS')
    wg_peers: str = Field(env='WG_PEERS')
    conf_dir: str = Field(env='CONF_DIR')

    host: str = Field(env='HOST')
    mysql_user: str = Field(env='MYSQL_USER')
    password: str = Field(env='PASSWORD')
    port: int = Field(env='PORT')
    mysql_database: str = Field(env='MYSQL_DATABASE')
    
    class Config:
        env_file = '.env'
        env_file_encoding = 'utf-8'

config = Settings()
