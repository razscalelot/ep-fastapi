from typing import List
from pydantic import BaseSettings, AnyHttpUrl
from decouple import config
from pymongo import MongoClient


class Settings(BaseSettings):
    APP_URL = config("APP_URL", cast=str)
    PORT: int = config("PORT", cast=int)
    API_VI_STR: str = "/api/v1"
    JWT_SECRET_KEY: str = config("JWT_SECRET_KEY", cast=str)
    JWT_REFRESH_SECRET_KEY: str =config("JWT_REFRESH_SECRET_KEY", cast=str)
    ALGORITHM = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 15
    REFRESH_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 7 # 7 Days
    BACKEND_CORS_ORIGINS: List[AnyHttpUrl] = []
    PROJECT_NAME: str = "EP-FASTAPI"
    FACTOR_URL: str = config("FACTOR_URL", cast=str)

    #Database
    MONGO_CONNECTION_STRING: str = config("MONGO_CONNECTION_STRING", cast=str)

    class Config:
        case_sensitive = True

settings = Settings()