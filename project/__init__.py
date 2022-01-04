import os
from pathlib import Path
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bootstrap import Bootstrap

app = Flask(__name__, static_folder="static")

Bootstrap(app)

app.config["SECRET_KEY"] = "chiavesupersegreta"

basedir = os.path.abspath(os.path.dirname(__file__))
app.config ["SQLALCHEMY_DATABASE_URI"] = "sqlite:///" + os.path.join(basedir, "db.sqlite")

app.config["SQLALCHEMY_TRSCK_MODIFICATIONS"] = False

db = SQLAlchemy(app)
