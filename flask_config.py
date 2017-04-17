import os
basedir = os.path.abspath(os.path.dirname(__file__))

SECRET_KEY = 'SCE'
CSRF_ENABLED = True
WTF_CSRF_SECRET_KEY = 'MY_SECRET_KEY'
SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'app.db')
SQLALCHEMY_MIGRATE_REPO = os.path.join(basedir, 'db_repository')
SQLALCHEMY_TRACK_MODIFICATIONS = False
