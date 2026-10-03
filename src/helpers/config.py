from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    app_name: str = "App Name"
    app_version: str = "1.0.0"
    openai_api_key: str
    file_allowed_extensions: list = []
    file_max_size: int = 5

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


def get_settings():
    return Settings()