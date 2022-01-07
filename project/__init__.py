import os
from pathlib import Path
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bootstrap import Bootstrap
from flask_mail import Mail

app = Flask(__name__, static_folder="static")

Bootstrap(app)

app.config["SECRET_KEY"] = "chiavesupersegreta"

basedir = os.path.abspath(os.path.dirname(__file__))
app.config ["SQLALCHEMY_DATABASE_URI"] = "sqlite:///" + os.path.join(basedir, "db.sqlite")

app.config["SQLALCHEMY_TRSCK_MODIFICATIONS"] = False

db = SQLAlchemy(app)

app.config['MAIL_SERVER']='smtp.gmail.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USERNAME'] = 'unibuddywebsite@gmail.com'
app.config['MAIL_PASSWORD'] = 'Studygroup1!'
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USE_SSL'] = True

mail=Mail()
