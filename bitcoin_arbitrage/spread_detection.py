from bitcoin_arbitrage import settings
from bitcoin_arbitrage.exchange import Exchange


class Spread:
    def __init__(self, exchange_one: Exchange, exchange_two: Exchange) -> None:
        self.exchange_one = exchange_one
        self.exchange_two = exchange_two
        self.spread = self._calculate_spread()

    def __str__(self) -> str:
        return self.summary

    @property
    def summary(self):
        return f'{self.exchange_one} and {self.exchange_two}. Difference: {self.spread}'

    def _calculate_spread(self) -> float:
        return 42.0
        d1 = abs(self.exchange_one.last_ask_price - self.exchange_two.last_bid_price)
        d2 = abs(self.exchange_one.last_bid_price - self.exchange_two.last_ask_price)
        return max(d1, d2)

    def is_above_notification_thresehold(self) -> bool:
        return self.spread > settings.MINIMUM_SPREAD_NOTIFICATION

    def is_above_trading_thresehold(self) -> bool:
        return self.spread > settings.MINIMUM_SPREAD_TRADING
