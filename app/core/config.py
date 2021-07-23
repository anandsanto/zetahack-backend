from typing import Any, Dict, List, Optional, Union
from pydantic import AnyHttpUrl, BaseSettings, validator
from pathlib import Path


class Settings(BaseSettings):
    PROJECT_NAME: str
    HOST: str = '0.0.0.0'
    PORT: int = '8080'
    WORKERS_PER_CORE: int = 1
    GRACEFULTIMEOUT: int = 120
    TIMEOUT: int = 120
    KEEPALIVE: int
    BACKEND_CORS_ORIGINS: List[AnyHttpUrl] = []
    PRODUCTION: bool
    MONGODB_URI: str
    MONGODB_NAME: str
    LOGGER_LEVEL: str
    ACCESSLOG: Path

    class Config:
        case_sensitive = True
        env_file = ".env"


settings = Settings()
