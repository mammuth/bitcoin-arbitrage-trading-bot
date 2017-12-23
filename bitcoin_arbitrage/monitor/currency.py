from enum import Enum

BTCAmount = float
FiatAmount = float


class CurrencyPair(Enum):
    BTC_USD = "BTC/USD"
    BTC_EUR = "BTC/EUR"

    BCH_USD = "BCH/USD"
    BCH_EUR = "BCH/EUR"

    ETH_USD = "ETH/USD"
    ETH_EUR = "ETH/EUR"

    @property
    def fiat_symbol(self):
        if self in [CurrencyPair.BTC_EUR, CurrencyPair.BCH_EUR, CurrencyPair.ETH_EUR]:
            return '€'
        elif self in [CurrencyPair.BTC_USD, CurrencyPair.BCH_USD, CurrencyPair.ETH_USD]:
            return '$'
