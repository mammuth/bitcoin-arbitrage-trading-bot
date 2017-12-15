from typing import List

from bitcoin_arbitrage.currency_pair import CurrencyPair
from bitcoin_arbitrage.exchange import Exchange
from bitcoin_arbitrage.exchange.bitstamp import Bitstamp

EXCHANGES: List[Exchange] = [
    Bitstamp(CurrencyPair.BTC_EUR),
]