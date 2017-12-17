from typing import List, Optional

from exchange import Exchange
from currency import BTCAmount, FiatAmount
import settings
from log import setup_logger
from order import Order
from spread_detection import Spread
from update import UpdateAction

logger = setup_logger('Trader')


class Trade:
    def __init__(self) -> None:
        self.buy_order: Order
        self.sell_order: Order


class Trader(UpdateAction):

    def __init__(self, spread_threshold: Optional[int] = None) -> None:
        super().__init__(spread_threshold)
        self.best_spread = None

    def run(self, spreads: List[Spread], exchanges: List[Exchange], timestamp: float) -> None:
        # Get best spread of this update
        spreads.sort(key=lambda x: x.spread, reverse=True)
        self.best_spread = spreads[0]

        # Evaluate opportunity and execute trade
        if self._should_use_this_spread() is True:
            self._make_trade()

    def _should_use_this_spread(self) -> bool:
        def _get_available_balance() -> BTCAmount:
            """
            Get the fiat and btc balance of the two exchanges
            and calculate the maximum available BTC amount which can be bought with that.
            """
            raise NotImplementedError

        def _calculate_expected_fees() -> FiatAmount:
            raise NotImplementedError

        def _calculate_expected_revenue() -> FiatAmount:
            raise NotImplementedError

        def _calculate_order_amount() -> BTCAmount:
            raise NotImplementedError

        available_balance = _get_available_balance()
        order_amount = _calculate_order_amount(available_balance)
        expected_fees = _calculate_expected_fees()
        expected_profit = _calculate_expected_revenue() - expected_fees

        # ToDo: Single formula

        if expected_profit < settings.PROFIT_THRESHOLD:
            logger.info(f'Not executing order since the expected profit {expected_profit} '
                        f'is below the threshold {settings.PROFIT_THRESHOLD}')

        return True

    def _make_trade(self) -> Trade:
        raise NotImplementedError
