from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bootstrap import Bootstrap
from flask_mail import Mail
from project.config import Config

app = Flask(__name__)
app.config.from_object(Config)

db = SQLAlchemy(app)
mail = Mail(app)

from project.users.routes import users
from project.groups.routes import meets
from project.main.routes import main

app.register_blueprint(users)
app.register_blueprint(meets)
app.register_blueprint(main)

Bootstrap(app)