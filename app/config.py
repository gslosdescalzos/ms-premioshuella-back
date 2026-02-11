from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    DATABASE_URL: str = "mysql+mysqlconnector://root:root@localhost:3306/premios_huella"

    GOOGLE_CLIENT_ID: str = ""
    GOOGLE_CLIENT_SECRET: str = ""
    GOOGLE_REDIRECT_URI: str = "http://localhost:8000/api/v1/auth/google/callback"

    JWT_SECRET_KEY: str = "change-me-in-production"
    JWT_ALGORITHM: str = "HS256"
    JWT_EXPIRATION_MINUTES: int = 60

    UPLOAD_DIR: str = "./uploads"

    API_V1_PREFIX: str = "/api/v1"

    model_config = {"env_file": ".env", "extra": "ignore"}


settings = Settings()
