from typing import List

from exchange import Exchange
from log import setup_logger
from spread_detection import Spread
from update.notification import NotificationService

logger = setup_logger('Stdout')


class StdoutNotification(NotificationService):
    def run(self, spreads: List[Spread], exchanges: List[Exchange], timestamp: float) -> None:
        if not self._should_notify():
            return
        spread = self._get_spread_for_notification(spreads)
        if spread is not None:
            print(f'BTC Spread {spread.spread_verbose} - {spread.summary}')
