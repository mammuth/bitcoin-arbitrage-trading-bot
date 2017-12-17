from abc import ABC, abstractmethod
from typing import Optional

from currency import CurrencyPair, BTCAmount
from order import OrderId


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

    @abstractmethod
    def limit_buy_order(self, amount: BTCAmount, limit: float) -> OrderId:
        raise NotImplementedError

    @abstractmethod
    def limit_sell_order(self, amount: BTCAmount, limit: float) -> OrderId:
        raise NotImplementedError

    # @abstractmethod
    # def get_order_status(self, id: OrderId) -> OrderStatus:
    #     raise NotImplementedError

    # @abstractmethod
    # def get_account_balance(self) -> float:
    #     raise NotImplementedError('Implement get_account_balance() for your exchange.')
    #
