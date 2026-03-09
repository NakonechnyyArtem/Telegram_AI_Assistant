from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    BOT_TOKEN: str
    GEMINI_API_KEY: str
    DB_HOST: str="localhost"
    DB_PORT: int=5432
    DB_USER: str="postgres"
    DB_PASSWORD: str=("mypassword")
    DB_NAME: str="mybot_db"

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"

settings = Settings()
