from dotenv import load_dotenv
import os

load_dotenv()

# #executing different directories project
# from pathlib import Path

# load_dotenv(Path(__file__).resolve().parent.parent / ".env")


class Settings:
    SQLALCHEMY_DATABASE_URL: str = os.getenv("SQLALCHEMY_DATABASE_URL")
    DATABASE_URL: str = os.getenv("DATABASE_URL")
    SECRET_KEY: str = os.getenv("SECRET_KEY")
    ALGORITHM: str = os.getenv("ALGORITHM", "HS256")
    ACCESS_TOKEN_EXPIRE_MINUTES: int = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES"))
    REFRESH_EXPIRE_DAYS: int = int(os.getenv("REFRESH_EXPIRE_DAYS"))
    FERNET_KEY: str = os.getenv("FERNET_KEY")
    MASTER_KEY: str = os.getenv("MASTER_KEY")

settings = Settings()