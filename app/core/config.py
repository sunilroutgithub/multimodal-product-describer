from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """
    Centralized application configuration.
    Values are loaded from the .env file, with environment variables
    taking priority if both are present (useful for deployment platforms
    like Hugging Face Spaces, which inject secrets as env vars).
    """

    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    GROQ_API_KEY: str
    HF_TOKEN: str | None = None
    APP_PORT: int = 8001
    MAX_BATCH_SIZE: int = 100


# Single shared instance imported throughout the app
settings = Settings()