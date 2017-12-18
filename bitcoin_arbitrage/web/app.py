import csv

from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from logging import Formatter, FileHandler
import logging
import os

app = Flask(__name__)
app.config.from_object('config')
db = SQLAlchemy(app)


# Tear down SQLAlchemy
@app.teardown_request
def shutdown_session(exception=None):
    db.session.remove()


@app.route('/')
def index():
    with open(app.config.get('LAST_SPREADS_FILENAME')) as f:
        last_spreads = [{k: v for k, v in row.items()} for row in csv.DictReader(f, skipinitialspace=True)]
    return render_template('index.html', last_spreads=last_spreads)


@app.route('/all-spreads')
def all_spreads():
    with open(app.config.get('SPREAD_HISTORY_FILENAME')) as f:
        spreads = [{k: v for k, v in row.items()} for row in csv.DictReader(f, skipinitialspace=True)]
    return render_template('alls_spreads.html', spreads=spreads)


# Error
@app.errorhandler(403)
def not_found_error(error):
    return render_template('page_403.html'), 403


@app.errorhandler(404)
def not_found_error(error):
    return render_template('page_404.html'), 404


@app.errorhandler(500)
def internal_error(error):
    return render_template('page_500.html'), 500


# Logs
if not app.debug:
    file_handler = FileHandler('error.log')
    format = '%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]'
    file_handler.setFormatter(Formatter(format))
    app.logger.setLevel(logging.INFO)
    file_handler.setLevel(logging.INFO)
    app.logger.addHandler(file_handler)
    app.logger.info('errors')

if __name__ == '__main__':
    # run on port 5000 by default
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
