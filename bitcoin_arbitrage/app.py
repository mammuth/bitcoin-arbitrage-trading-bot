import asyncio
import csv
from datetime import date
from threading import Thread
from typing import List

from flask import Flask, render_template, Response
from flask_sqlalchemy import SQLAlchemy
from logging import Formatter, FileHandler
import logging
import os
from sqlalchemy import Date, cast, and_, extract

from bitcoin_arbitrage import config

app = Flask(__name__)
app.config.from_object(config)
db = SQLAlchemy(app)


# Tear down SQLAlchemy
@app.teardown_request
def shutdown_session(exception=None):
    db.session.remove()


@app.route('/')
def realtime():
    from bitcoin_arbitrage.models import Spread
    last_spreads: List[Spread] = Spread.query\
        .order_by(Spread.id.desc())\
        .limit(4)\
        .from_self().order_by(Spread.spread.desc())\
        .all()
    return render_template('index.html', spreads=last_spreads)


def _spreads_list_view(queryset: SQLAlchemy.Query) -> Response:
    from bitcoin_arbitrage.models import Spread
    all = queryset.order_by(Spread.id.desc()).all()
    highest = queryset.order_by(Spread.spread.desc()).first()
    lowest = queryset.order_by(Spread.spread.asc()).first()
    return render_template('spreads_list.html', spreads=all, highest=highest, lowest=lowest)


@app.route('/today')
def today():
    from bitcoin_arbitrage.models import Spread
    now = date.today()
    todays_spreads_query = Spread.query.filter(
        and_(
            now.year == extract('year', Spread.recorded_date),
            now.month == extract('month', Spread.recorded_date),
            now.day == extract('day', Spread.recorded_date)
        )
    )
    return _spreads_list_view(todays_spreads_query)


@app.route('/all-spreads')
def all_spreads():
    from bitcoin_arbitrage.models import Spread
    spreads_query = Spread.query
    return _spreads_list_view(spreads_query)


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
    # file_handler = FileHandler('error.log')
    # format = '%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]'
    # file_handler.setFormatter(Formatter(format))
    # app.logger.setLevel(logging.INFO)
    # file_handler.setLevel(logging.INFO)
    # app.logger.addHandler(file_handler)
    # app.logger.info('errors')
    from bitcoin_arbitrage.monitor.log import setup_logger
    app.logger = setup_logger('App')


def start_monitor_thread(loop):
    from bitcoin_arbitrage.monitor.monitor import Monitor
    print('start monitor thread')
    app.logger.info('start monitor thread')
    monitor = Monitor()
    try:
        loop.run_until_complete(monitor.update())
    except Exception:
        import traceback
        print('Exception im monitor. Stacktrace:')
        app.logger.error('Exception im monitor. Stacktrace:')
        print(traceback.format_exc())
        app.logger.error(traceback.format_exc())


if __name__ == '__main__':
    monitor_loop = asyncio.get_event_loop()
    t = Thread(target=start_monitor_thread, args=(monitor_loop,))
    t.start()

    port = int(os.environ.get('FLASK_PORT', 5000))
    # reloader=True may result in start_monitor_thread called multiple times
    app.run(host='0.0.0.0', port=port, debug=app.config.get('DEBUG'), use_reloader=False)
