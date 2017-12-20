from typing import List

from bitcoin_arbitrage.monitor.exchange import Exchange
from bitcoin_arbitrage.monitor.log import setup_logger
from bitcoin_arbitrage.monitor.spread_detection import Spread
from bitcoin_arbitrage.monitor.update.notification import NotificationService

logger = setup_logger('Stdout')


class StdoutNotification(NotificationService):
    def run(self, spreads: List[Spread], exchanges: List[Exchange], timestamp: float) -> None:
        if not self._should_notify(0):
            return
        spread = self._get_spread_for_notification(spreads)
        if spread is not None:
            print(f'Spread {spread.spread_with_currency} - {spread.summary}')
