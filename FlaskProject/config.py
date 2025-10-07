import os

class Config:
    SECRET_KEY = os.environ.get("Mariela", "super secret key")
    SQLALCHEMY_DATABASE_URI = os.environ.get("DATABASE_URL", "sqlite:///app.db")
    SQLALCHEMY_TRACK_MODIFICATIONS = False