import logging

import pushbullet as pb_lib

from bitcoin_arbitrage.notification import NotificationService
from bitcoin_arbitrage.spread_detection import Spread

logger = logging.Logger('Pushbullet')
logger.setLevel(logging.DEBUG)


class Pushbullet(NotificationService):

    def __init__(self, api_key) -> None:
        super().__init__()
        # ToDo: Raise error when api key is missing
        if api_key == 'DEBUG':
            self._pb = None
        else:
            self._pb = pb_lib.Pushbullet(api_key=api_key)

    def notify(self, spread: Spread) -> None:
        logger.debug('Notifying...')
        if self._pb is not None:
            self._pb.push_note(title='BTC Arbitrage', body=f'{spread.summary}')

