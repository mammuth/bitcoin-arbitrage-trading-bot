from abc import ABC, abstractmethod

from bitcoin_arbitrage.currency_pair import CurrencyPair


class Exchange(ABC):
    currency_pair: CurrencyPair

    def __init__(self, currency_pair: CurrencyPair):
        self.currency_pair = currency_pair

    def __str__(self):
        return f"{self.name} ({self.currency_pair.value})" \
               f"\n - Ask: {self.get_ask_price()}" \
               f"\n - Bid: {self.get_bid_price()}"

    @property
    def name(self) -> str:
        return str(self.__class__.__name__)

    @property
    @abstractmethod
    def currency_pair_api_representation(self) -> str:
        raise NotImplementedError

    @property
    @abstractmethod
    def base_url(self) -> str:
        raise NotImplementedError

    @abstractmethod
    def get_ask_price(self) -> float:
        return NotImplemented

    @abstractmethod
    def get_bid_price(self) -> float:
        return NotImplemented
