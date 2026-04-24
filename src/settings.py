from typing import ClassVar

from pydantic_settings import BaseSettings, SettingsConfigDict


class Setting(BaseSettings):
    model_config: ClassVar[SettingsConfigDict] = SettingsConfigDict(
        env_file=".env")

    SWAGGER: str | None = None
    REDOCS: str | None = None
    ROOT_PATH: str
    BD_NAME: str
    BD_HOST: str
    BD_PORT: str
    BD_USERNAME: str
    BD_PASSWORD: str
    SECRET_KEY: str
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60
    JWT_ALGORITHM: str = "HS256"
    API_PREFIX: str = "/api/v1"


setting: Setting = Setting()  # type: ignore
