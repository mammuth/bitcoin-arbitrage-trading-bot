from enum import Enum


class CurrencyPair(Enum):
    BTC_USD = "BTC/USD"
    BTC_EUR = "BTC/EUR"

    BCH_USD = "BCH/USD"
    BCH_EUR = "BCH/EUR"

    ETH_USD = "ETH/USD"
    ETH_EUR = "ETH/EUR"

    @property
    def fiat_symbol(self):
        if self == CurrencyPair.BTC_EUR:
            return '€'
        elif self == CurrencyPair.BTC_USD:
            return '$'
