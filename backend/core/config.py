from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    PROJECT_NAME: str = "AHTSE"
    VERSION: str = "1.0.0"
    API_V1_STR: str = "/api"

    # Firewall Defaults
    DEFAULT_MODE: str = "balanced"

    # Logging
    LOG_LEVEL: str = "INFO"

    class Config:
        case_sensitive = True


settings = Settings()
