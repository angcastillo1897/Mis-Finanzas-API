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


setting: Setting = Setting()  # type: ignore
