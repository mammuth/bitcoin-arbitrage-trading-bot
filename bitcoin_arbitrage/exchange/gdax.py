import logging
import requests

from currency_pair import CurrencyPair
from exchange import Exchange

logger = logging.Logger('gdax')


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
        json = response.json()
        self.last_ask_price = float(json.get('ask'))
        self.last_bid_price = float(json.get('bid'))

