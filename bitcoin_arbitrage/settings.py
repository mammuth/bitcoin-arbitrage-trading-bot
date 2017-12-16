import logging
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
    StdoutNotification(spread_threshold=300),
]

UPDATE_INTERVAL = 5  # seconds

PRICE_HISTORY_FILE = 'price_history.csv'
SPREAD_HISTORY_FILE = 'spread_history.csv'
SPREAD_HISTORY_THRESHOLD = 200


MINIMUM_SPREAD_TRADING = 200

LOG_LEVEL = logging.DEBUG
