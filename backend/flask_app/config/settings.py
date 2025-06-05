import os

class Config:
    DEBUG = True
    DB_URI = os.getenv("DB_URI", "sqlite:///sage.db")
    SQLALCHEMY_DATABASE_URI = DB_URI
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    UPLOAD_FOLDER = os.getenv("UPLOAD_FOLDER", "./data/uploaded")
