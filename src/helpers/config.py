from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    app_name: str 
    app_version: str
    openai_api_key: str
    file_allowed_types: list
    file_max_size: int
    upload_dir: str
    file_default_chunk_size: int
    mongodb_uri: str
    mongodb_db_name: str

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


def get_settings():
    return Settings()