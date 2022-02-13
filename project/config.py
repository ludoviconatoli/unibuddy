import os

class Config:
    basedir = os.path.abspath(os.path.dirname(__file__))
    SECRET_KEY = "chiavesupersegreta"
    SQLALCHEMY_DATABASE_URI = "sqlite:///" + os.path.join(basedir, "db.sqlite")
    SQLALCHEMY_TRSCK_MODIFICATIONS = False
    MAIL_SERVER = 'smtp.gmail.com'
    MAIL_PORT = 587
    MAIL_USERNAME = 'unibuddywebsite@gmail.com'
    MAIL_PASSWORD = 'Studygroup1!'
    MAIL_USE_TLS = True