from pydantic_settings import BaseSettings 

class Settings(BaseSettings):
    PROJECT_NAME: str = "FinGuard"
    DATABASE_URL: str 
    REDIS_URL: str 
    ENVIRONMENT: str = "development"

    CELERY_RESULT_BACKEND: str 

    POSTGRES_USER:str
    POSTGRES_PASSWORD:str
    POSTGRES_DB:str
    SECRET_KEY: str 

    TEST_POSTGRES_USER: str
    TEST_POSTGRES_PASSWORD: str
    TEST_POSTGRES_DB: str

    PEPPER_ENV_KEY:str 
    OTP_SECRET_KEY: str
    class Config: 
        env_file = ".env"
        env_file_encoding = "utf-8"


settings = Settings()