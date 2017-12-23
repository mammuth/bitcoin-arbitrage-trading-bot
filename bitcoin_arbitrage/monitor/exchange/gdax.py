import base64
import datetime
import hmac

import hashlib
import requests
from requests.auth import AuthBase

from bitcoin_arbitrage.monitor import settings
from bitcoin_arbitrage.monitor.currency import CurrencyPair
from bitcoin_arbitrage.monitor.exchange import Exchange, BTCAmount
from bitcoin_arbitrage.monitor.log import setup_logger
from bitcoin_arbitrage.monitor.order import Order, OrderState, OrderId

logger = setup_logger('gdax')


# Create custom authentication
class GdaxAuth(AuthBase):
    def __init__(self):
        self.api_key = settings.GDAX_KEY
        self.secret_key = settings.GDAX_SECRET
        self.passphrase = settings.GDAX_PASSPHRASE

    def __call__(self, request):
        timestamp = str(datetime.time())
        message = timestamp + request.method + request.path_url + (request.body or '')
        hmac_key = base64.b64decode(self.secret_key)
        signature = hmac.new(hmac_key, message, hashlib.sha256)
        signature_b64 = signature.digest().encode('base64').rstrip('\n')

        request.headers.update({
            'CB-ACCESS-SIGN': signature_b64,
            'CB-ACCESS-TIMESTAMP': timestamp,
            'CB-ACCESS-KEY': self.api_key,
            'CB-ACCESS-PASSPHRASE': self.passphrase,
            'Content-Type': 'application/json'
        })
        return request


class Gdax(Exchange):
    base_url = "https://api.gdax.com"

    currency_pair_api_representation = {
        CurrencyPair.BTC_USD: "BTC-USD",
        CurrencyPair.BTC_EUR: "BTC-EUR",

        CurrencyPair.ETH_USD: "ETH-USD",
        CurrencyPair.ETH_EUR: "ETH-EUR",
    }

    def __init__(self, currency_pair: CurrencyPair):
        super().__init__(currency_pair)
        self.auth = GdaxAuth()

    @property
    def ticker_url(self) -> str:
        return f"{self.base_url}/products/{self.currency_pair_api_representation[self.currency_pair]}/ticker"

    def _place_limit_order(self, side: str, amount: BTCAmount, limit: float) -> OrderId:
        url = f"{self.base_url}/orders/"
        data = {
            'product_id': self.currency_pair_api_representation.get(self.currency_pair),
            'side': side,
            'size': amount,
            'price': limit,
        }
        response = requests.post(url, json=data, auth=self.auth)
        json = response.json()
        order_id = json.get('id')
        return order_id

    def limit_sell_order(self, amount: BTCAmount, limit: float) -> Order:
        order_id = self._place_limit_order('sell', amount, limit)
        return Order(exchange=self, order_id=order_id)

    def limit_buy_order(self, amount: BTCAmount, limit: float) -> Order:
        order_id = self._place_limit_order('buy', amount, limit)
        return Order(exchange=self, order_id=order_id)

    def get_order_state(self, order: Order) -> OrderState:
        raise NotImplementedError
