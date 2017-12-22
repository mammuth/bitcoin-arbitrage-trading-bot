from bitcoin_arbitrage.monitor.currency import CurrencyPair
from bitcoin_arbitrage.monitor.exchange import Exchange, BTCAmount, OrderId
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

    @property
    def ticker_url(self):
        return f"{self.base_url}/pubticker/{self.currency_pair_api_representation[self.currency_pair]}"

    def limit_sell_order(self, amount: BTCAmount, limit: float) -> OrderId:
        raise NotImplementedError

    def limit_buy_order(self, amount: BTCAmount, limit: float) -> OrderId:
        raise NotImplementedError
