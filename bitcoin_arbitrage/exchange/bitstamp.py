import logging

import requests

from bitcoin_arbitrage.currency_pair import CurrencyPair
from bitcoin_arbitrage.exchange import Exchange

logger = logging.Logger('Bitstamp')


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
