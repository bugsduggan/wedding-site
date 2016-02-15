import os

from flask import Flask
from flask_bootstrap import Bootstrap
from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.login import LoginManager


db = SQLAlchemy()
lm = LoginManager()


def create_app(config=None):
    app = Flask(__name__)

    app.config.from_object('wedding_site.default_config')
    if 'WEDDING_SITE_CONFIG' in os.environ:
        app.config.from_envvar('WEDDING_SITE_CONFIG')
    if config:
        app.config.from_object(config)

    app.logger.setLevel(app.config['LOG_LEVEL'])

    db.init_app(app)

    lm.init_app(app)
    lm.login_view = 'frontend.oauth_authorize'
    lm.login_message = None

    Bootstrap(app)

    from wedding_site.views.frontend import frontend
    app.register_blueprint(frontend)
    from wedding_site.views.admin import admin
    app.register_blueprint(admin)
    from wedding_site.views.api import api
    app.register_blueprint(api)

    return app
