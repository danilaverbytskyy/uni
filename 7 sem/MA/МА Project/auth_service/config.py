import os

def build_db_uri() -> str:
    host = os.getenv("DB_HOST", "localhost")
    port = os.getenv("DB_PORT", "5432")
    name = os.getenv("DB_NAME", "user_platform")
    user = os.getenv("DB_USER", "postgres")
    password = os.getenv("DB_PASSWORD", "postgres")
    return f"postgresql+psycopg://{user}:{password}@{host}:{port}/{name}"

class Config:
    SECRET_KEY = os.getenv("FLASK_SECRET_KEY", "dev-secret-key-change-me")
    SQLALCHEMY_DATABASE_URI = build_db_uri()
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    PROFILE_SERVICE_URL = os.getenv("PROFILE_SERVICE_URL", "http://profile-service:5000")

    LOGIN_TITLE = os.getenv("LOGIN_TITLE", "Вход в систему")
    REGISTER_TITLE = os.getenv("REGISTER_TITLE", "Регистрация")
    WELCOME_MESSAGE = os.getenv("WELCOME_MESSAGE", "Добро пожаловать в платформу")
