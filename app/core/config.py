from pydantic_settings import BaseSettings
from pydantic import PostgresDsn


class Settings(BaseSettings):
    # Postgresql
    DB_USERNAME: str
    DB_PASSWORD: str
    DB_HOST: str = "localhost"
    DB_PORT: int = 5432
    DB_NAME: str
    DB_ECHO: bool = False

    # Настройки JWT авторизации
    JWT_SECRET_KEY: str = ""
    JWT_ALGORITHM: str = "HS256"

    # Настройки Endpoints
    HOUSE_INFO_ENDPOINT: str = "http://127.0.0.1:8000/api/houses"
    MESSAGES_ENDPOINT: str = "http://127.0.0.1:8010/api/messages"
    USER_INFO_ENDPOINT: str = "http://127.0.0.1:8030/api/users"

    # Ключи доступа ко внутренним сервисам
    SENDER_API_KEY: str = ""
    AUTH_API_KEY: str = ""

    class Config:
        env_file = ".env"

    @property
    def database_url(self) -> PostgresDsn:
        return PostgresDsn.build(
            scheme="postgresql+psycopg",
            username=self.DB_USERNAME,
            password=self.DB_PASSWORD,
            host=self.DB_HOST,
            port=self.DB_PORT,
            path=self.DB_NAME
        )

settings = Settings()
