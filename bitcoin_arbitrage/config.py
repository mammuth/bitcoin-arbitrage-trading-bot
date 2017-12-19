import os

basedir = os.path.abspath(os.path.dirname(__file__))
SQLALCHEMY_TRACK_MODIFICATIONS = False
SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'database.db')
SECRET_KEY = 'secret_key_here'
DEBUG = True

LAST_SPREADS_FILENAME = 'last_spreads.csv'
SPREAD_HISTORY_FILENAME = 'spread_history.csv'
