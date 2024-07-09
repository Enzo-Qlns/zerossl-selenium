from pydantic import BaseSettings


class Settings(BaseSettings):
    APP_ENV: str = 'dev'

    class Config:
        env_file = '.env'


settings = Settings()
