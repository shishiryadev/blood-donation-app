import os

class Config:
    SECRET_KEY = os.environ.get("SECRET_KEY", "dev_secret_change_me")
    DATABASE_URL = os.environ.get(
        "DATABASE_URL",
        "postgresql+psycopg2://postgres:*your-postgres-password*@localhost:5432/blood_donation_db"
    )
    SQLALCHEMY_DATABASE_URI = DATABASE_URL.replace("postgres://", "postgresql+psycopg2://")
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    JWT_SECRET_KEY = os.environ.get("JWT_SECRET_KEY", "jwt_dev_secret_change_me")
    CORS_ORIGINS = os.environ.get("CORS_ORIGINS", "*")
