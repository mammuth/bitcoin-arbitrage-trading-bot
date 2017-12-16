import logging
from typing import List

from exchange import Exchange
from spread_detection import Spread
from update.notification import NotificationService

logger = logging.Logger('Pushbullet')
logger.setLevel(logging.DEBUG)


class StdoutNotification(NotificationService):
    def run(self, spreads: List[Spread], exchanges: List[Exchange], timestamp: float) -> None:
        for spread in spreads:
            if self._should_notify(spread=spread):
                print(spread.summary)
