from pydantic import BaseSettings

class Settings(BaseSettings):
    # Here you would put things like:
    # openai_api_key: str | None = None
    # db_url: str = "postgresql+psycopg://..."
    env: str = "dev"

    class Config:
        env_file = ".env"


settings = Settings()
