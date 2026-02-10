import os

class Config:
    SECRET_KEY = os.getenv("SECRET_KEY", "dev-secret-key-change-me")

    # Example: postgresql+psycopg2://user:pass@localhost:5432/user_platform
    SQLALCHEMY_DATABASE_URI = os.getenv(
        "DATABASE_URL",
        "postgresql+psycopg2://postgres:postgres@localhost:5432/user_platform",
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # UI texts (handy for ConfigMap ui-config in k8s)
    LOGIN_TITLE = os.getenv("LOGIN_TITLE", "Вход в систему")
    REGISTER_TITLE = os.getenv("REGISTER_TITLE", "Регистрация")
    WELCOME_MESSAGE = os.getenv("WELCOME_MESSAGE", "Добро пожаловать в платформу")
