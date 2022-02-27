import os

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bootstrap import Bootstrap
from flask_mail import Mail

from project.config import config

#app = Flask(__name__)
#app.config.from_object(Config)

#db = SQLAlchemy(app)
#mail = Mail(app)

bootstrap = Bootstrap()
db = SQLAlchemy()
mail = Mail()

#app.register_blueprint(users)
#app.register_blueprint(meets)
#app.register_blueprint(main)
#app.register_blueprint(errors)

#Bootstrap(app)
def create_app(config_name):
    app = Flask(__name__, static_folder="static")
    app.config.from_object(config[config_name])
    config[config_name].init_app(app)

    bootstrap.init_app(app)
    db.init_app(app)
    mail.init_app(app)

    from project.users.routes import users
    from project.groups.routes import meets
    from project.main.routes import main
    from project.errors.handlers import errors

    app.register_blueprint(users)
    app.register_blueprint(meets)
    app.register_blueprint(main)
    app.register_blueprint(errors)

    return app
