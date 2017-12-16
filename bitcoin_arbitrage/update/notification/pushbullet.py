import logging
from typing import List

import pushbullet as pb_lib

from exchange import Exchange
from spread_detection import Spread
from update.notification import NotificationService

logger = logging.Logger('Pushbullet')
logger.setLevel(logging.DEBUG)


class Pushbullet(NotificationService):
    def __init__(self, spread_threshold: float, api_key: str) -> None:
        super().__init__(spread_threshold)
        # ToDo: Raise error when api key is missing
        if api_key == 'DEBUG':
            self._pb = None
        else:
            self._pb = pb_lib.Pushbullet(api_key=api_key)

    def run(self, spreads: List[Spread], exchanges: List[Exchange], timestamp: float) -> None:
        for spread in spreads:
            if self._should_notify(spread=spread):
                logger.debug('Notifying...')
                if self._pb is not None:
                    self._pb.push_note(title=f'BTC Spread {spread.spread_verbose}', body=f'{spread.summary}')
