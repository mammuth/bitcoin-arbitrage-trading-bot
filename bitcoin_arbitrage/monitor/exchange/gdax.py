import requests

from bitcoin_arbitrage.monitor.currency_pair import CurrencyPair
from bitcoin_arbitrage.monitor.exchange import Exchange, OrderId, BTCAmount, OrderSide
from bitcoin_arbitrage.monitor.log import setup_logger

logger = setup_logger('gdax')


class Gdax(Exchange):
    base_url = "https://api.gdax.com"

    currency_pair_api_representation = {
        CurrencyPair.BTC_USD: "BTC-USD",
        CurrencyPair.BTC_EUR: "BTC-EUR"
    }

    def ticker_url(self):
        return f"{self.base_url}/products/{self.currency_pair_api_representation[self.currency_pair]}/ticker"

    def place_limit_order(self, side: OrderSide, amount: BTCAmount, limit: float,
                          currency_pair: CurrencyPair) -> OrderId:
        url = f"{self.base_url}/orders/"
        response = requests.post(url, data={
            'product_id': self.currency_pair_api_representation.get(currency_pair),
            'side': 'buy',
            'size': amount,
            'price': limit,
            # 'cancel_after': ''  # ToDo
        })
        json = response.json()
        order_id = json.get('id')
        return order_id
