from enum import Enum


class CurrencyPair(Enum):
    BTC_USD = "BTC/USD"
    BTC_EUR = "BTC/EUR"

    @property
    def fiat_symbol(self):
        if self == CurrencyPair.BTC_EUR:
            return '€'
        elif self == CurrencyPair.BTC_USD:
            return '$'
