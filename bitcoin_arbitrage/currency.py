from enum import Enum

BTCAmount = float
FiatAmount = float


class CurrencyPair(Enum):
    BTC_USD = "BTC/USD"
    BTC_EUR = "BTC/EUR"
