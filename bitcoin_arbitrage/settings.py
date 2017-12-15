import logging
from typing import List

from currency_pair import CurrencyPair

from exchange import Exchange
from exchange.bitfinex import Bitfinex
from exchange.bitstamp import Bitstamp
from exchange.gdax import Gdax

from notification import NotificationService
from notification.pushbullet import Pushbullet

EXCHANGES: List[Exchange] = [
    Bitfinex(CurrencyPair.BTC_EUR),
    Bitstamp(CurrencyPair.BTC_EUR),
    Gdax(CurrencyPair.BTC_EUR),
]

NOTIFICATION_SERVICES: List[NotificationService] = [
    Pushbullet(api_key='DEBUG'),
]

UPDATE_INTERVAL = 5  # seconds

PRICE_HISTORY_FILE = 'price_history.csv'


MINIMUM_SPREAD_NOTIFICATION = 1
MINIMUM_SPREAD_TRADING = 200

LOG_LEVEL = logging.DEBUG
