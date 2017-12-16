import pytest

from bitcoin_arbitrage.log import setup_logger  # NOQA
from bitcoin_arbitrage.currency_pair import CurrencyPair
from bitcoin_arbitrage.exchange.bitstamp import Bitstamp
from bitcoin_arbitrage.spread_detection import Spread


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
    with pytest.raises(AttributeError):
        exchange_one = Bitstamp(CurrencyPair.BTC_EUR)
        exchange_one.last_ask_price = 14_500.0
        exchange_one.last_bid_price = 14_500.0
        exchange_two = Bitstamp(CurrencyPair.BTC_USD)
        exchange_two.last_ask_price = 14_600.0
        exchange_two.last_bid_price = 14_600.0

        Spread(exchange_one, exchange_two)
