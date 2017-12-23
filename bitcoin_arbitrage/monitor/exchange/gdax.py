import datetime
from typing import Dict, Any

import requests

from bitcoin_arbitrage.monitor import settings
from bitcoin_arbitrage.monitor.currency import CurrencyPair
from bitcoin_arbitrage.monitor.exchange import Exchange, BTCAmount
from bitcoin_arbitrage.monitor.log import setup_logger
from bitcoin_arbitrage.monitor.order import Order, OrderState, OrderId

logger = setup_logger('gdax')


class Gdax(Exchange):
    """
    Notes: Every private request needs to have the headers provided by _request_headers
    """
    base_url = "https://api.gdax.com"

    currency_pair_api_representation = {
        CurrencyPair.BTC_USD: "BTC-USD",
        CurrencyPair.BTC_EUR: "BTC-EUR",

        CurrencyPair.ETH_USD: "ETH-USD",
        CurrencyPair.ETH_EUR: "ETH-EUR",
    }

    @property
    def ticker_url(self) -> str:
        return f"{self.base_url}/products/{self.currency_pair_api_representation[self.currency_pair]}/ticker"

    def _place_limit_order(self, side: str, amount: BTCAmount, limit: float) -> OrderId:
        url = f"{self.base_url}/orders/"
        response = requests.post(url, json={
            'product_id': self.currency_pair_api_representation.get(self.currency_pair),
            'side': side,
            'size': amount,
            'price': limit,
        }, headers=self._request_headers)
        json = response.json()
        order_id = json.get('id')
        return order_id


    @property
    def _request_headers(self) -> Dict[str, Any]:
        return {
            'content-type': 'application/json',
            'CB-ACCESS-TIMESTAMP': datetime.datetime.now().timestamp(),
            'CB-ACCESS-KEY': settings.GDAX_KEY,
            'CB-ACCESS-SIGN': settings.GDAX_SIGNATURE,
            'CB-ACCESS-PASSPHRASE': settings.GDAX_SIGNATURE,
        }

    def limit_sell_order(self, amount: BTCAmount, limit: float) -> Order:
        order_id = self._place_limit_order('sell', amount, limit)
        return Order(exchange=self, order_id=order_id)

    def limit_buy_order(self, amount: BTCAmount, limit: float) -> Order:
        order_id = self._place_limit_order('buy', amount, limit)
        return Order(exchange=self, order_id=order_id)

    def get_order_state(self, order: Order) -> OrderState:
        raise NotImplementedError
