from typing import List

from currency_pair import CurrencyPair
from exchange import Exchange
from exchange.bitstamp import Bitstamp

EXCHANGES: List[Exchange] = [
    Bitstamp(CurrencyPair.BTC_EUR),
]
