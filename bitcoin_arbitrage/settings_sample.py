import logging

from update.spread_history import SpreadHistoryToCSV

LOG_LEVEL = logging.INFO

from typing import List

from currency_pair import CurrencyPair

from exchange import Exchange
from exchange.bitfinex import Bitfinex
from exchange.bitstamp import Bitstamp
from exchange.gdax import Gdax

from update import UpdateAction
from update.notification.pushbullet import Pushbullet
from update.notification.stdout import StdoutNotification

EXCHANGES: List[Exchange] = [
    Bitfinex(CurrencyPair.BTC_EUR),
    Bitstamp(CurrencyPair.BTC_EUR),
    Gdax(CurrencyPair.BTC_EUR),
]

UPDATE_ACTIONS: List[UpdateAction] = [
    Pushbullet(spread_threshold=500, api_key='DEBUG'),
    StdoutNotification(spread_threshold=100),
    SpreadHistoryToCSV(filename='spread_history.csv'),
]

UPDATE_INTERVAL = 30  # seconds

TIME_BETWEEN_NOTIFICATIONS = 5 * 60  # Only send a notification every 5 minutes

MINIMUM_SPREAD_TRADING = 200
