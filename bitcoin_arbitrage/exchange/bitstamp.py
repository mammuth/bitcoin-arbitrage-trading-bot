import requests

from bitcoin_arbitrage.currency_pair import CurrencyPair
from bitcoin_arbitrage.exchange import Exchange


class Bitstamp(Exchange):
    base_url = "https://www.bitstamp.net/api/v2"
    currency_pair_api_representation = {
        CurrencyPair.BTC_USD: "btcusd",
        CurrencyPair.BTC_EUR: "btceur"
    }
    currency_pair = None

    def get_ask_price(self) -> float:
        url = f"{self.base_url}/ticker/{self.currency_pair_api_representation[self.currency_pair]}"
        response = requests.get(url)
        json = response.json()
        return json.get('ask')

    def get_bid_price(self) -> float:
        url = f"{self.base_url}/ticker/{self.currency_pair_api_representation[self.currency_pair]}"
        response = requests.get(url)
        json = response.json()
        return json.get('bid')
