import os


basedir = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))

if os.environ.get('ON_HEROKU') is None:
    ON_HEROKU = False
else:
    ON_HEROKU = True

if os.environ.get('DATABASE_URL') is None:
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'data.db')
else:
    SQLALCHEMY_DATABASE_URI = os.environ['DATABASE_URL']
SQLALCHEMY_MIGRATE_REPO = os.path.join(basedir, 'db_repository')
SQLALCHEMY_TRACK_MODIFICATIONS = False

if ON_HEROKU:
    SECRET_KEY = os.environ['SECRET_KEY']
    DEBUG = False
    WTF_CSRF_SECRET_KEY = os.environ['WTF_CSRF_SECRET_KEY']
else:
    SECRET_KEY = 'changeme'
    DEBUG = True
    WTF_CSRF_SECRET_KEY = 'changeme'

LOG_LEVEL = 20

if ON_HEROKU:
    OAUTH_CREDENTIALS = {
        'google': {
            'id': os.environ['GOOGLE_CLIENT_ID'],
            'secret': os.environ['GOOGLE_CLIENT_SECRET']
        }
    }
else:
    OAUTH_CREDENTIALS = {
        'google': {
            'id': 'beepboop',
            'secret': 'boopbeep'
        }
    }
