from pydantic import BaseSettings


class Settings(BaseSettings):
    APP_ENV: str = 'dev'
    PASSWORD: str = 'Password123!'

    class Config:
        env_file = '.env'


settings = Settings()
