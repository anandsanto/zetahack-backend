from typing import Any, Dict, List, Optional, Union
from pydantic import AnyHttpUrl, BaseSettings, validator
from pathlib import Path
import os


# class Settings(BaseSettings):
#     PROJECT_NAME: str
#     HOST: str = '0.0.0.0'
#     PORT: int = '8080'
#     WORKERS_PER_CORE: int = 1
#     GRACEFULTIMEOUT: int = 120
#     TIMEOUT: int = 120
#     KEEPALIVE: int
#     BACKEND_CORS_ORIGINS: List[AnyHttpUrl] = []
#     PRODUCTION: bool
#     MONGODB_URI: str
#     MONGODB_NAME: str
#     LOGGER_LEVEL: str
#     ACCESSLOG: Path
#
#     class Config:
#         case_sensitive = True
#         env_file = ".env"
#
class Settings(BaseSettings):
    PROJECT_NAME: str = os.environ['PROJECT_NAME']
    HOST: str = os.environ['HOST']
    PORT: int = os.environ['PORT']
    WORKERS_PER_CORE: int = os.environ['WORKERS_PER_CORE']
    GRACEFULTIMEOUT: int = os.environ['GRACEFULTIMEOUT']
    TIMEOUT: int = os.environ['TIMEOUT']
    KEEPALIVE: int = os.environ['KEEPALIVE']
    BACKEND_CORS_ORIGINS: List[AnyHttpUrl] =  os.environ['BACKEND_CORS_ORIGINS']
    PRODUCTION: bool = os.environ['PRODUCTION']
    MONGODB_URI: str = os.environ['MONGODB_URI']
    MONGODB_NAME: str = os.environ['MONGODB_NAME']
    LOGGER_LEVEL: str = os.environ['LOGGER_LEVEL']
    ACCESSLOG: Path = os.environ['ACCESSLOG']

settings = Settings()
