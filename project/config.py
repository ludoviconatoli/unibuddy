import os
from pathlib import Path

basedir = os.path.abspath(os.path.dirname(__file__))

class Config:
    FLASK_CONFIG = os.environ.get("FLASK_CONFIG")
    DEBUG = os.environ.get("DEBUG")
    SECRET_KEY = "chiavesupersegreta"
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    MAIL_SERVER = 'smtp.gmail.com'
    MAIL_PORT = 587
    MAIL_USERNAME = 'unibuddywebsite@gmail.com'
    MAIL_PASSWORD = 'Studygroup1!'
    MAIL_USE_TLS = True
    @staticmethod
    def init_app(app):
        pass

class ProdConfig(Config):
    SQLALCHEMY_DATABASE_URI = os.environ.get("DATABASE_URL")
    DEBUG = False

class DevConfig(Config):
    SQLALCHEMY_DATABASE_URI = "sqlite:///" + os.path.join(basedir, "db.sqlite")
    DEBUG = True

config = {
    "development": DevConfig,
    "production": ProdConfig,
    "default": DevConfig
}