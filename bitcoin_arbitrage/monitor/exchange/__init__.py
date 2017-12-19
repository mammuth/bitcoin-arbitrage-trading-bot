from enum import Enum
import requests

from abc import ABC, abstractmethod
from typing import Optional

from bitcoin_arbitrage.monitor.currency_pair import CurrencyPair


OrderId = str
BTCAmount = float


class OrderSide(Enum):
    BUY = 'buy'
    SELL = 'sell'


class OrderStatus(Enum):
    PENDING = 'pending'
    DONE = 'done'
    CANCELLED = 'cancelled'


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

    @abstractmethod
    def ticker_url(self) -> str:
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
    def update_prices(self) -> None:
        response = requests.get(self.ticker_url())
        if response.status_code != 200:
            # logger.warning('Could not update prices. API returned status != 200.')
            return
        json = response.json()
        self.last_ask_price = float(json.get('ask'))
        self.last_bid_price = float(json.get('bid'))

    @abstractmethod
    def place_limit_order(self, side: OrderSide, amount: BTCAmount, limit: float,
                          currency_pair: CurrencyPair) -> OrderId:
        raise NotImplementedError

    # @abstractmethod
    # def get_order_status(self, id: OrderId) -> OrderStatus:
    #     raise NotImplementedError

    # @abstractmethod
    # def get_account_balance(self) -> float:
    #     raise NotImplementedError('Implement get_account_balance() for your exchange.')
    #
