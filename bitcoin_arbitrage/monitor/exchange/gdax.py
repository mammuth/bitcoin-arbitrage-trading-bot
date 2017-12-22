import requests

from bitcoin_arbitrage.monitor.currency import CurrencyPair
from bitcoin_arbitrage.monitor.exchange import Exchange, OrderId, BTCAmount
from bitcoin_arbitrage.monitor.log import setup_logger
from bitcoin_arbitrage.monitor.order import Order

logger = setup_logger('gdax')


class Gdax(Exchange):
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
        response = requests.post(url, data={
            'product_id': self.currency_pair_api_representation.get(self.currency_pair),
            'side': side,
            'size': amount,
            'price': limit,
            # 'cancel_after': ''  # ToDo
        })
        json = response.json()
        order_id = json.get('id')
        return order_id

    def limit_sell_order(self, amount: BTCAmount, limit: float) -> Order:
        order_id = self._place_limit_order('sell', amount, limit)
        return Order(exchange=self, order_id=order_id)

    def limit_buy_order(self, amount: BTCAmount, limit: float) -> Order:
        order_id = self._place_limit_order('buy', amount, limit)
        return Order(exchange=self, order_id=order_id)
