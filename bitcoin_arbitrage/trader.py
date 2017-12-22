from typing import List, Optional

from bitcoin_arbitrage.monitor import settings
from bitcoin_arbitrage.monitor.exchange import Exchange
from bitcoin_arbitrage.monitor.log import setup_logger
from bitcoin_arbitrage.monitor.spread_detection import Spread
from bitcoin_arbitrage.monitor.update import UpdateAction
from bitcoin_arbitrage.monitor.order import Order

logger = setup_logger('Trader')


class Trade:
    def __init__(self, sell_order: Order, buy_order: Order) -> None:
        self.sell_order = sell_order
        self.buy_order = buy_order


class Trader(UpdateAction):

    def __init__(self, spread_threshold: Optional[int] = None) -> None:
        super().__init__(spread_threshold)
        self.spread: Spread = None
        self.enabled = True  # Trader will get disabled after we executed a trade.
        # Restart is required to make the trader actually trade again

    def run(self, spreads: List[Spread], exchanges: List[Exchange], timestamp: float) -> None:
        # Get best spread of this update
        spreads.sort(key=lambda x: x.spread, reverse=True)
        self.spread = spreads[0]

        # Evaluate opportunity and execute trade
        if self._should_use_this_spread() is True:
            trade = self._make_trade()
            self.enabled = False
            self._store_trade(trade)

    def _should_use_this_spread(self) -> bool:
        above_spread_limit = self.spread.spread > settings.MINIMUM_SPREAD_TRADING
        return self.enabled and above_spread_limit

    def _make_trade(self) -> Trade:
        # ToDo Test
        btc_order_amount = settings.TRADING_BTC_AMOUNT

        # Sell Order
        sell_limit = self.spread.exchange_sell.last_bid_price - settings.TRADING_LIMIT_PUFFER
        sell_order: Order = self.spread.exchange_sell.limit_buy_order(btc_order_amount, sell_limit)

        # ToDo: Only buy if the sell order is fulfilled?

        # Buy Order
        buy_limit = self.spread.exchange_buy.last_ask_price + settings.TRADING_LIMIT_PUFFER
        buy_order: Order = self.spread.exchange_buy.limit_buy_order(btc_order_amount, buy_limit)

        return Trade(sell_order=sell_order, buy_order=buy_order)

    def _store_trade(self, trade: Trade) -> None:
        pass  # ToDo
