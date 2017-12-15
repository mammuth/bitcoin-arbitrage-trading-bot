import logging
from typing import List

from currency_pair import CurrencyPair
from exchange import Exchange
from exchange.bitstamp import Bitstamp
from notification import NotificationService
from notification.pushbullet import Pushbullet

EXCHANGES: List[Exchange] = [
    Bitstamp(CurrencyPair.BTC_EUR),
    Bitstamp(CurrencyPair.BTC_USD),  # Doesn't make any sense, but we want two exchanges :)
]

NOTIFICATION_SERVICES: List[NotificationService] = [
    Pushbullet(api_key='DEBUG'),
]

UPDATE_INTERVAL = 5  # seconds

PRICE_HISTORY_FILE = 'price_history.csv'


MINIMUM_SPREAD_NOTIFICATION = 1
MINIMUM_SPREAD_TRADING = 500

LOG_LEVEL = logging.DEBUG
