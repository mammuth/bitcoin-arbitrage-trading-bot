import logging
from typing import List

from currency_pair import CurrencyPair

from exchange import Exchange
from exchange.bitfinex import Bitfinex
from exchange.bitstamp import Bitstamp
from exchange.gdax import Gdax

from notification import NotificationService
from notification.pushbullet import Pushbullet
from notification.stdout import StdoutNotification

EXCHANGES: List[Exchange] = [
    Bitfinex(CurrencyPair.BTC_EUR),
    Bitstamp(CurrencyPair.BTC_EUR),
    Gdax(CurrencyPair.BTC_EUR),
]

NOTIFICATION_SERVICES: List[NotificationService] = [
    Pushbullet(spread_threshold=500, api_key='DEBUG'),
    StdoutNotification(spread_threshold=300),
]

UPDATE_INTERVAL = 5  # seconds

PRICE_HISTORY_FILE = 'price_history.csv'
SPREAD_HISTORY_FILE = 'spread_history.csv'
SPREAD_HISTORY_THRESHOLD = 200


MINIMUM_SPREAD_TRADING = 200

LOG_LEVEL = logging.DEBUG
