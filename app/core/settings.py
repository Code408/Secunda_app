from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    DATABASE_URL: str = "mysql+aiomysql://root:12345@127.0.0.1:3306/secunda"
    # API-ключ для простейшей аутентификации
    API_KEY: str = "test-api-key"

    class Config:
        env_file = ".env"

# Инициализация настроек
settings = Settings()