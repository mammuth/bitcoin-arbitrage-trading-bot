import requests

from currency import CurrencyPair
from exchange import Exchange, OrderId, BTCAmount
from log import setup_logger

logger = setup_logger('gdax')


class Gdax(Exchange):
    base_url = "https://api.gdax.com"
    currency_pair_api_representation = {
        CurrencyPair.BTC_USD: "BTC-USD",
        CurrencyPair.BTC_EUR: "BTC-EUR"
    }

    # Todo: Make async
    def update_prices(self) -> None:
        url = f"{self.base_url}/products/{self.currency_pair_api_representation[self.currency_pair]}/ticker"
        response = requests.get(url)
        if response.status_code != 200:
            logger.warning('Could not update prices. API returned status != 200.')
            return
        json = response.json()
        self.last_ask_price = float(json.get('ask'))
        self.last_bid_price = float(json.get('bid'))

    def limit_buy_order(self, amount: BTCAmount, limit: float) -> OrderId:
        return self._execute_limit_order('buy', amount, limit)

    def limit_sell_order(self, amount: BTCAmount, limit: float) -> OrderId:
        return self._execute_limit_order('sell', amount, limit)

    def _execute_limit_order(self, side: str, amount: BTCAmount, limit: float) -> OrderId:
        currency_slug = self.currency_pair_api_representation[self.currency_pair]
        url = f"{self.base_url}/orders/"
        response = requests.post(url, data={
            'product_id': currency_slug,
            'side': side,
            'size': amount,
            'price': limit,
            # 'cancel_after': ''  # ToDo
        })
        json = response.json()
        order_id = json.get('id')
        return order_id
