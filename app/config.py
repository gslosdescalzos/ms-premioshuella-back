from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    DATABASE_URL: str
    SUPABASE_JWT_SECRET: str
    AWS_ACCESS_KEY_ID: str
    AWS_SECRET_ACCESS_KEY: str
    AWS_REGION: str = "eu-west-1"
    AWS_S3_BUCKET: str = "premios-huella-participations"
    ALLOWED_ORIGINS: str = "http://localhost:4321"
    API_V1_PREFIX: str = "/api/v1"

    @property
    def allowed_origins_list(self) -> list[str]:
        return [
            origin.strip()
            for origin in self.ALLOWED_ORIGINS.split(",")
            if origin.strip()
        ]

    model_config = {"env_file": ".env", "extra": "ignore"}


settings = Settings()
