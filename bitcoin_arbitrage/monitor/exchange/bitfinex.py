from bitcoin_arbitrage.monitor.currency_pair import CurrencyPair
from bitcoin_arbitrage.monitor.exchange import Exchange, OrderSide, BTCAmount, OrderId
from bitcoin_arbitrage.monitor.log import setup_logger

logger = setup_logger('Bitfinex')


class Bitfinex(Exchange):
    base_url = "https://api.bitfinex.com/v1"

    currency_pair_api_representation = {
        CurrencyPair.BTC_USD: "BTCUSD",
        CurrencyPair.BTC_EUR: "BTCEUR",

        CurrencyPair.ETH_USD: "ETHUSD",
        # CurrencyPair.ETH_EUR: "ETHEUR",  # Does not exist apparently
    }

    def ticker_url(self):
        return f"{self.base_url}/pubticker/{self.currency_pair_api_representation[self.currency_pair]}"

    def place_limit_order(self, side: OrderSide, amount: BTCAmount, limit: float,
                          currency_pair: CurrencyPair) -> OrderId:
        raise NotImplementedError
