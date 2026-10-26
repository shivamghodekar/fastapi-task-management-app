from pydantic_settings import BaseSettings,SettingsConfigDict

class Setting(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env",extra="ignore")

    DB_CONNECTIONS: str
    SECRET_KEY: str
    ALGORITHM: str
    EXP_TIME: int

settings=Setting()

