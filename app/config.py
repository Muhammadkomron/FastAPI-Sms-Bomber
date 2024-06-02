import logging
from logging.config import dictConfig
from pathlib import Path

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict

logging_config = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "default": {
            "format": "%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        },
    },
    "handlers": {
        "console": {
            "class": "logging.StreamHandler",
            "formatter": "default",
        },
    },
    "root": {
        "level": "INFO",
        "handlers": ["console"],
    },
}

dictConfig(logging_config)
logger = logging.getLogger(__name__)


class Settings(BaseSettings):
    DATABASE_URL: str
    SECRET_KEY: str
    DEBUG: bool
    REDIS_HOST: str
    ESKIZ_HOST: str
    ESKIZ_EMAIL: str
    ESKIZ_PASSWORD: str
    ESKIZ_TOKEN_KEY: str

    model_config = SettingsConfigDict(
        env_file=Path(__file__).resolve().parent.parent / '.env',
        env_file_encoding='utf-8',
        extra='allow',
    )

    # class Config:
    #     env_file = Path(__file__).resolve().parent.parent / '.env'


settings = Settings()
