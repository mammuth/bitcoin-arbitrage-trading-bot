import pytest

from bitcoin_arbitrage.monitor import settings  # NOQA
from bitcoin_arbitrage.monitor.log import setup_logger  # NOQA
from bitcoin_arbitrage.monitor.log import setup_logger  # NOQA
from bitcoin_arbitrage.monitor.currency import CurrencyPair
from bitcoin_arbitrage.monitor.exchange.bitstamp import Bitstamp
from bitcoin_arbitrage.monitor.spread_detection import Spread
from bitcoin_arbitrage.monitor.spread_detection import SpreadDifferentCurrenciesError


def test_calculate_spread():
    exchange_one = Bitstamp(CurrencyPair.BTC_EUR)
    exchange_one.last_ask_price = 14_500.0
    exchange_one.last_bid_price = 14_500.0
    exchange_two = Bitstamp(CurrencyPair.BTC_EUR)
    exchange_two.last_ask_price = 14_600.0
    exchange_two.last_bid_price = 14_600.0
    spread = Spread(exchange_one, exchange_two)
    assert spread.spread == 100

    exchange_one = Bitstamp(CurrencyPair.BTC_EUR)
    exchange_one.last_ask_price = 14_600.0
    exchange_one.last_bid_price = 14_600.0
    exchange_two = Bitstamp(CurrencyPair.BTC_EUR)
    exchange_two.last_ask_price = 14_500.0
    exchange_two.last_bid_price = 14_500.0
    spread = Spread(exchange_one, exchange_two)
    assert spread.spread == 100

    exchange_one = Bitstamp(CurrencyPair.BTC_EUR)
    exchange_one.last_ask_price = 14_600.0
    exchange_one.last_bid_price = 14_500.0
    exchange_two = Bitstamp(CurrencyPair.BTC_EUR)
    exchange_two.last_ask_price = 14_600.0
    exchange_two.last_bid_price = 14_500.0
    spread = Spread(exchange_one, exchange_two)
    assert spread.spread == -100

    exchange_one = Bitstamp(CurrencyPair.BTC_EUR)
    exchange_one.last_ask_price = 14_600.0
    exchange_one.last_bid_price = 14_500.0
    exchange_two = Bitstamp(CurrencyPair.BTC_EUR)
    exchange_two.last_ask_price = 14_500.0
    exchange_two.last_bid_price = 14_600.0
    spread = Spread(exchange_one, exchange_two)
    assert spread.spread == 0


def test_different_currencies_exception():
    exchange_one = Bitstamp(CurrencyPair.BTC_EUR)
    exchange_one.last_ask_price = 14_500.0
    exchange_one.last_bid_price = 14_500.0
    exchange_two = Bitstamp(CurrencyPair.BTC_USD)
    exchange_two.last_ask_price = 14_600.0
    exchange_two.last_bid_price = 14_600.0
    with pytest.raises(SpreadDifferentCurrenciesError):
        Spread(exchange_one, exchange_two)
