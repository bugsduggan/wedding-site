import os


basedir = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))

SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'data.db')
SQLALCHEMY_MIGRATE_REPO = os.path.join(basedir, 'db_repository')
SQLALCHEMY_TRACK_MODIFICATIONS = False

SECRET_KEY = 'changeme'
DEBUG = True
LOG_LEVEL = 20

WTF_CSRF_SECRET_KEY = 'changeme'

OAUTH_CREDENTIALS = {
    'google': {
        'id': 'beepboop',
        'secret': 'boopbeep'
    }
}
