import json
import sys
import requests

from abc import ABC, abstractmethod
from typing import Optional

from bitcoin_arbitrage.monitor.currency import CurrencyPair, BTCAmount
from bitcoin_arbitrage.monitor.order import Order, OrderState

from bitcoin_arbitrage.monitor.log import setup_logger

logger = setup_logger('Exchange')


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

    @property
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
        response = requests.get(self.ticker_url)
        if response.status_code != 200:
            logger.warning('Could not update prices. API returned status != 200.')
            return
        try:
            json_response = response.json()
            self.last_ask_price = float(json_response.get('ask'))
            self.last_bid_price = float(json_response.get('bid'))
        except json.decoder.JSONDecodeError or TypeError:
            logger.error('Could not update prices. Error on json processing:')
            logger.error(sys.exc_info())

    @abstractmethod
    def limit_buy_order(self, amount: BTCAmount, limit: float) -> Order:
        raise NotImplementedError

    @abstractmethod
    def limit_sell_order(self, amount: BTCAmount, limit: float) -> Order:
        raise NotImplementedError

    def get_order_state(self, order: Order) -> OrderState:
        raise NotImplementedError

    def cancel_order(self, order: Order) -> None:
        raise NotImplementedError

    # @abstractmethod
    # def get_account_balance(self) -> FiatAmount:
    #     raise NotImplementedError('Implement get_account_balance() for your exchange.')
    #
