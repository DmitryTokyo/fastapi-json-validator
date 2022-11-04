from pydantic import BaseSettings


class Settings(BaseSettings):
    PROJECT_NAME: str = 'Restaurant schedule representation'
    API_V1_STR: str = '/api/v1'


settings = Settings()
