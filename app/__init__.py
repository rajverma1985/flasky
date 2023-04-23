from flask import Flask, abort, render_template, redirect, url_for, session
from flask_bootstrap import Bootstrap
from flask_mail import Mail, Message
from flask_sqlalchemy import SQLAlchemy
from flask_moment import Moment
from config import config

bootstrap = Bootstrap()
moment = Moment()
mail = Mail()
db = SQLAlchemy()


def create_app(config_name):
    app = Flask(__name__)
    app.config.from_object(config[config_name])
    config[config_name].init_app(app)

    bootstrap.init_app(app)
    moment.init_app(app)
    mail.init_app(app)
    db.init_app(app)

    # placeholder for custom app error codes

    return app
