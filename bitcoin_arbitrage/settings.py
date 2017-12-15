import logging
from typing import List

from bitcoin_arbitrage.currency_pair import CurrencyPair
from bitcoin_arbitrage.exchange import Exchange
from bitcoin_arbitrage.exchange.bitstamp import Bitstamp
from bitcoin_arbitrage.notification import NotificationService
from bitcoin_arbitrage.notification.pushbullet import Pushbullet

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
