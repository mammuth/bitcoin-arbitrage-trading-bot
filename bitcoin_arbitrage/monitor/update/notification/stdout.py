from typing import List

from monitor.exchange import Exchange
from monitor.log import setup_logger
from monitor.spread_detection import Spread
from monitor.update.notification import NotificationService

logger = setup_logger('Stdout')


class StdoutNotification(NotificationService):
    def run(self, spreads: List[Spread], exchanges: List[Exchange], timestamp: float) -> None:
        if not self._should_notify(0):
            return
        spread = self._get_spread_for_notification(spreads)
        if spread is not None:
            print(f'BTC Spread {spread.spread_verbose} - {spread.summary}')
