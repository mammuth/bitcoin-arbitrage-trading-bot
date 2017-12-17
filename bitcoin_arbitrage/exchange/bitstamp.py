import requests

from currency import CurrencyPair
from exchange import Exchange, OrderId, BTCAmount
from log import setup_logger

logger = setup_logger('Bitstamp')


class Bitstamp(Exchange):
    base_url = "https://www.bitstamp.net/api/v2"
    currency_pair_api_representation = {
        CurrencyPair.BTC_USD: "btcusd",
        CurrencyPair.BTC_EUR: "btceur"
    }

    # Todo: Make async
    def update_prices(self) -> None:
        url = f"{self.base_url}/ticker/{self.currency_pair_api_representation[self.currency_pair]}"
        response = requests.get(url)
        if response.status_code != 200:
            logger.warning('Could not update prices. API returned status != 200.')
            return
        json = response.json()
        self.last_ask_price = float(json.get('ask'))
        self.last_bid_price = float(json.get('bid'))

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

    def limit_buy_order(self, amount: BTCAmount, limit: float) -> OrderId:
        return self._execute_limit_order('buy', amount, limit)

    def limit_sell_order(self, amount: BTCAmount, limit: float) -> OrderId:
        return self._execute_limit_order('sell', amount, limit)

    def _execute_limit_order(self, side: str, amount: BTCAmount, limit: float,
                             currency_pair: CurrencyPair) -> OrderId:
        currency_slug = self.currency_pair_api_representation[self.currency_pair]
        url = f"{self.base_url}/{side.value}/{currency_slug}/"
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
