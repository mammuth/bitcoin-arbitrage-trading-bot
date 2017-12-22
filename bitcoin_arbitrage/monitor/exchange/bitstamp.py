import requests

from bitcoin_arbitrage.monitor.currency import CurrencyPair
from bitcoin_arbitrage.monitor.exchange import Exchange, OrderId, BTCAmount
from bitcoin_arbitrage.monitor.log import setup_logger

logger = setup_logger('Bitstamp')


class Bitstamp(Exchange):
    base_url = "https://www.bitstamp.net/api/v2"

    currency_pair_api_representation = {
        CurrencyPair.BTC_USD: "btcusd",
        CurrencyPair.BTC_EUR: "btceur",

        CurrencyPair.ETH_USD: "ethusd",
        CurrencyPair.ETH_EUR: "etheur",
    }

    @property
    def ticker_url(self):
        return f"{self.base_url}/ticker/{self.currency_pair_api_representation[self.currency_pair]}"

    def get_account_balance(self) -> float:
        url = f"{self.base_url}/balance/"
        response = requests.post(url, data={
            'key': '',
            'signature': '',
            'nonce': ''
        })
        json = response.json()
        eur_balance = float(json.get('eur_balance'))
        return eur_balance

    def _place_limit_order(self, side: str, amount: BTCAmount, limit: float) -> OrderId:
        url = f"{self.base_url}/{side}/{self.currency_pair_api_representation[self.currency_pair]}/"
        response = requests.post(url, data={
            'key': '',
            'signature': '',
            'nonce': '',
            'amount': amount,
            'price': '',
            'limit_price': limit
        })
        json = response.json()
        order_id = json.get('id')
        return order_id

    def limit_sell_order(self, amount: BTCAmount, limit: float) -> OrderId:
        return self._place_limit_order('sell', amount, limit)

    def limit_buy_order(self, amount: BTCAmount, limit: float) -> OrderId:
        return self._place_limit_order('buy', amount, limit)


