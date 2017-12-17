import requests

from currency import CurrencyPair, BTCAmount
from exchange import Exchange
from log import setup_logger
from order import OrderId

logger = setup_logger('Bitfinex')


class Bitfinex(Exchange):

    base_url = "https://api.bitfinex.com/v1"
    currency_pair_api_representation = {
        CurrencyPair.BTC_USD: "BTCUSD",
        CurrencyPair.BTC_EUR: "BTCEUR"
    }

    # Todo: Make async
    def update_prices(self) -> None:
        url = f"{self.base_url}/pubticker/{self.currency_pair_api_representation[self.currency_pair]}"
        response = requests.get(url)
        if response.status_code != 200:
            logger.warning('Could not update prices. API returned status != 200.')
            return
        json = response.json()
        self.last_ask_price = float(json.get('ask'))
        self.last_bid_price = float(json.get('bid'))

    def limit_buy_order(self, amount: BTCAmount, limit: float) -> OrderId:
        raise NotImplementedError

    def limit_sell_order(self, amount: BTCAmount, limit: float) -> OrderId:
        raise NotImplementedError
