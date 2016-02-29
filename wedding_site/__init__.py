import os

from flask import Flask
from flask_bootstrap import Bootstrap
from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.login import LoginManager

from wedding_site.utils import CustomJSONEncoder
from wedding_site.utils.filters import momentjs


db = SQLAlchemy()
lm = LoginManager()


def load_models():
    from wedding_site.models import user, group, invitation, todo


load_models()


def init_extensions(app):
    db.init_app(app)

    lm.init_app(app)
    lm.login_view = 'frontend.oauth_authorize'
    lm.login_message = None

    Bootstrap(app)


def init_views(app):
    from wedding_site.views.frontend import frontend
    app.register_blueprint(frontend)
    from wedding_site.views.admin import admin
    app.register_blueprint(admin)
    from wedding_site.views.api import api
    app.register_blueprint(api)


def create_app(config=None):
    app = Flask(__name__)

    app.config.from_object('wedding_site.default_config')
    if 'WEDDING_SITE_CONFIG' in os.environ:
        app.config.from_envvar('WEDDING_SITE_CONFIG')
    if config:
        app.config.from_object(config)

    app.logger.setLevel(app.config['LOG_LEVEL'])
    app.json_encoder = CustomJSONEncoder
    app.jinja_env.globals['momentjs'] = momentjs

    init_extensions(app)
    init_views(app)

    return app
