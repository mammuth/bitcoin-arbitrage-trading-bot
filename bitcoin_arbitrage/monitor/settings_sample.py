import logging

import os

LOG_LEVEL = logging.INFO

from typing import List

from bitcoin_arbitrage.monitor.currency import CurrencyPair

from bitcoin_arbitrage.monitor.exchange import Exchange
from bitcoin_arbitrage.monitor.exchange.bitfinex import Bitfinex
from bitcoin_arbitrage.monitor.exchange.bitstamp import Bitstamp
from bitcoin_arbitrage.monitor.exchange.gdax import Gdax

from bitcoin_arbitrage.monitor.update import UpdateAction
from bitcoin_arbitrage.monitor.update.db_commit import SpreadHistoryToDB
from bitcoin_arbitrage.monitor.update.notification.pushbullet import Pushbullet
from bitcoin_arbitrage.monitor.update.notification.stdout import StdoutNotification
from bitcoin_arbitrage.monitor.update.csv_writer import SpreadHistoryToCSV, LastSpreadsToCSV

EXCHANGES: List[Exchange] = [
    Bitfinex(CurrencyPair.BTC_EUR),

    Bitstamp(CurrencyPair.BTC_EUR),
    Bitstamp(CurrencyPair.ETH_EUR),

    Gdax(CurrencyPair.BTC_EUR),
    Gdax(CurrencyPair.ETH_EUR),
]

UPDATE_ACTIONS: List[UpdateAction] = [
    Pushbullet(spread_threshold=500, api_key='DEBUG'),
    StdoutNotification(spread_threshold=100),
    SpreadHistoryToDB(),
]

UPDATE_INTERVAL = 30  # seconds

TIME_BETWEEN_NOTIFICATIONS = 5 * 60  # Only send a notification every 5 minutes

MINIMUM_SPREAD_TRADING = 200
TRADING_BTC_AMOUNT = 0.5
TRADING_LIMIT_PUFFER = 10  # Fiat Amount
TRADING_ORDER_STATE_UPDATE_INTERVAL = 1
TRADING_TIME_UNTIL_ORDER_CANCELLATION = 30

GDAX_KEY = os.environ.get('GDAX_KEY')
GDAX_SECRET = os.environ.get('GDAX_SECRET')
GDAX_PASSPHRASE = os.environ.get('GDAX_PASSPHRASE')
