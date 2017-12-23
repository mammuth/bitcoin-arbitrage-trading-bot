from bitcoin_arbitrage.monitor.currency import CurrencyPair
from bitcoin_arbitrage.monitor.exchange import Exchange, BTCAmount
from bitcoin_arbitrage.monitor.log import setup_logger
from bitcoin_arbitrage.monitor.order import Order, OrderState

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
    def ticker_url(self) -> str:
        return f"{self.base_url}/pubticker/{self.currency_pair_api_representation[self.currency_pair]}"

    def limit_sell_order(self, amount: BTCAmount, limit: float) -> Order:
        raise NotImplementedError

    def limit_buy_order(self, amount: BTCAmount, limit: float) -> Order:
        raise NotImplementedError

    def get_order_state(self, order: Order) -> OrderState:
        raise NotImplementedError
