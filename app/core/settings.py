from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    DATABASE_URL: str = "mysql+aiomysql://root:12345@mysql:3306/secunda?charset=utf8mb4"
    API_KEY: str = "test-api-key"

    class Config:
        env_file = ".env"

# Инициализация настроек
settings = Settings()
