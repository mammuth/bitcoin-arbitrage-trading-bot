from typing import List

from exchange import Exchange
from log import setup_logger
from spread_detection import Spread
from update.notification import NotificationService

logger = setup_logger('Stdout')


class StdoutNotification(NotificationService):
    def run(self, spreads: List[Spread], exchanges: List[Exchange], timestamp: float) -> None:
        for spread in spreads:
            if self._should_notify(spread=spread):
                print(spread.summary)
