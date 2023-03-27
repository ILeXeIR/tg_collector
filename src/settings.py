import secrets

from pydantic import BaseSettings


class Settings(BaseSettings):

    TG_BOT_TOKEN: str

    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60
    ALGORITHM: str = "HS256"

    SECRET_KEY: str

    WEBHOOK_HOST: str
    WEBHOOK_PATH: str
    WEBHOOK_TOKEN: str = secrets.token_hex(16)

    POSTGRES_USER: str
    POSTGRES_PASSWORD: str
    POSTGRES_HOST: str
    POSTGRES_PORT: int = 5432
    POSTGRES_DB: str

    class Config:
        env_file = ".env"

    @property
    def webhook_url(self) -> str:
        return f"{self.WEBHOOK_HOST}{self.WEBHOOK_PATH}"

    @property
    def postgresql_url(self) -> str:
        return f"postgres://{self.POSTGRES_USER}:" \
               f"{self.POSTGRES_PASSWORD}@{self.POSTGRES_HOST}:" \
               f"{self.POSTGRES_PORT}/{self.POSTGRES_DB}"


settings = Settings()
