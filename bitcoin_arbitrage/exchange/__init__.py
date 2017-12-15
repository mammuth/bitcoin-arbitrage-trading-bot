from abc import ABC, abstractmethod
from typing import Optional

from currency_pair import CurrencyPair


class Exchange(ABC):

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

    def __init__(self, currency_pair: CurrencyPair):
        self.currency_pair = currency_pair
        self.last_ask_price: Optional[float] = None
        self.last_bid_price: Optional[float] = None

    def __str__(self):
        return f"{self.name} ({self.currency_pair.value})"

    @property
    def summary(self):
        return self.__str__() + f"\n - Ask: {self.last_ask_price}" \
                                f"\n - Bid: {self.last_bid_price}"

    # ToDo: Make async
    @abstractmethod
    def update_prices(self) -> None:
        raise NotImplementedError('Implement update_prices() for your exchange. '
                                  'Make sure to also set self.last_ask_price and self.last_bid_price at the end.')
