import logging
import requests

from currency_pair import CurrencyPair
from exchange import Exchange
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

    def buy(self) -> str:
        url = f"{self.base_url}/buy/{self.currency_pair}/"
        response = requests.post(url, data={
            'key': '',
            'signature': '',
            'nonce': '',
            'amount': '',
            'price': '',
            'limit_price': ''
        })
        json = response.json()
        order_id = json.get('id')
        return order_id
