from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    PROJECT_NAME: str = "Sistema de Gestión  API"
    DATABASE_URL: str = "sqlite:///./sql_app.db"
    SECRET_KEY: str = "cl4v3_s3cr3t4_5up3r_53gur4_p4r4_p0rtfol10"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30

    class Config:
        env_file = ".env"

settings = Settings()