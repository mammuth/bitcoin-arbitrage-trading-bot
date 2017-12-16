from typing import List

import pushbullet as pb_lib

import settings
from log import setup_logger

from exchange import Exchange
from spread_detection import Spread
from update.notification import NotificationService

logger = setup_logger('Pushbullet')


class Pushbullet(NotificationService):
    def __init__(self, spread_threshold: int, api_key: str) -> None:
        super(Pushbullet, self).__init__(spread_threshold)
        # ToDo: Raise error when api key is missing
        if api_key == 'DEBUG':
            self._pb = None
        else:
            self._pb = pb_lib.Pushbullet(api_key=api_key)

    def run(self, spreads: List[Spread], exchanges: List[Exchange], timestamp: float) -> None:
        if not self._should_notify(settings.TIME_BETWEEN_NOTIFICATIONS):
            return
        spread = self._get_spread_for_notification(spreads)
        if spread is not None:
            logger.info('Notifying about spread via Pushbullet')
            if self._pb is not None:
                self._pb.push_note(title=f'BTC Spread {spread.spread_verbose}', body=f'{spread.summary}')
