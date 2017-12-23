import time
from enum import Enum
from typing import List, Optional

from bitcoin_arbitrage.monitor import settings
from bitcoin_arbitrage.monitor.exchange import Exchange
from bitcoin_arbitrage.monitor.log import setup_logger
from bitcoin_arbitrage.monitor.spread_detection import Spread
from bitcoin_arbitrage.monitor.update import UpdateAction
from bitcoin_arbitrage.monitor.order import Order, OrderState

logger = setup_logger('Trader')


class Trade:
    def __init__(self, sell_order: Order, buy_order: Order) -> None:
        self.sell_order = sell_order
        self.buy_order = buy_order


class TraderState(Enum):
    READY = 0
    TRADE_PENDING = 1
    TRADE_DONE = 2


class Trader(UpdateAction):

    def __init__(self, spread_threshold: Optional[int] = None) -> None:
        super().__init__(spread_threshold)
        self.spread: Spread = None
        self.state = TraderState.READY
        # Restart is required to make the trader actually trade again

    def run(self, spreads: List[Spread], exchanges: List[Exchange], timestamp: float) -> None:
        if self.state is TraderState.READY:
            # Get best spread of this update
            spreads.sort(key=lambda x: x.spread, reverse=True)
            self.spread = spreads[0]

            # Evaluate opportunity
            if self._should_use_this_spread() is True:
                return

            # Execute trade
            trade = self._make_trade()
            self._store_trade(trade)
            return

        if self.state in [TraderState.TRADE_DONE, TraderState.TRADE_PENDING]:
            logger.info('Not doing anything, since trader is not ready, but trade is done or pending.')
            return

    def _should_use_this_spread(self) -> bool:
        above_spread_limit = self.spread.spread > settings.MINIMUM_SPREAD_TRADING
        return self.state == TraderState.READY and above_spread_limit

    def _make_trade(self) -> Trade:
        # ToDo Test / Review / Make sure we don't fuck up
        btc_order_amount = settings.TRADING_BTC_AMOUNT

        # Sell Order
        sell_limit = self.spread.exchange_sell.last_bid_price - settings.TRADING_LIMIT_PUFFER
        sell_order: Order = self.spread.exchange_sell.limit_buy_order(btc_order_amount, sell_limit)
        sell_order_state = self.spread.exchange_sell.get_order_state(sell_order)

        self.state = TraderState.TRADE_PENDING

        while sell_order_state is OrderState.PENDING:
            sell_order_state = self.spread.exchange_sell.get_order_state(sell_order)
            time.sleep(settings.TRADING_ORDER_STATE_UPDATE_INTERVAL)

        if sell_order_state is OrderState.CANCELLED:
            # ToDo: How to handle this?
            logger.warning('Sell Order is cancelled.')

        if sell_order_state is OrderState.DONE:
            # Buy Order
            buy_limit = self.spread.exchange_buy.last_ask_price + settings.TRADING_LIMIT_PUFFER
            buy_order: Order = self.spread.exchange_buy.limit_buy_order(btc_order_amount, buy_limit)
            buy_order_state = self.spread.exchange_buy.get_order_state(buy_order)

            while buy_order_state is OrderState.PENDING:
                buy_order_state = self.spread.exchange_buy.get_order_state(buy_order)
                time.sleep(settings.TRADING_ORDER_STATE_UPDATE_INTERVAL)

            self.state = TraderState.TRADE_DONE
            return Trade(sell_order=sell_order, buy_order=buy_order)

    def _store_trade(self, trade: Trade) -> None:
        pass  # ToDo
