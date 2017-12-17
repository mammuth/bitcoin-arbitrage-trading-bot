import requests

from currency_pair import CurrencyPair
from exchange import Exchange, OrderSide, BTCAmount, OrderId
from log import setup_logger

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

    def place_limit_order(self, side: OrderSide, amount: BTCAmount, limit: float,
                          currency_pair: CurrencyPair) -> OrderId:
        raise NotImplementedError