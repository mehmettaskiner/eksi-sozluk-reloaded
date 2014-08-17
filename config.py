# some settings
import os

basedir = os.path.abspath(os.path.dirname(__file__))

# form config
CSRF_ENABLED = True
SECRET_KEY = 'undecryptable-secret-key'

# sqlite
SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'app.db')
SQLALCHEMY_MIGRATE_REPO = os.path.join(basedir, 'db_repository')
