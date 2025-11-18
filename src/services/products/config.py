from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    # These are the variables Pydantic will read from your .env file
    SECRET_KEY: str
    ALGORITHM: str

    # This tells Pydantic to read from a file named .env
    model_config = SettingsConfigDict(env_file=".env")

# Create a single, global instance of your settings
# You will import this 'settings' object in other files
settings = Settings()