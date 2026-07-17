from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    app_name: str = "Universal AI Code Review Assistant"
    max_file_size_mb: int = 2


settings = Settings()