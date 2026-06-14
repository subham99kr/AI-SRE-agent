from pydantic_settings import BaseSettings


class Settings(BaseSettings):

    GEMINI_API_KEY: str

    POSTGRES_HOST: str = "localhost"

    POSTGRES_PORT: int = 5433

    POSTGRES_DB: str = "ai_sre"

    POSTGRES_USER: str = "postgres"

    POSTGRES_PASSWORD: str = "postgres"

    class Config:
        env_file = ".env"


settings = Settings()

AUTO_APPROVE = True      # Use this only for Development