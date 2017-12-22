from typing import List

import pushbullet as pb_lib
from pushbullet import PushError

from bitcoin_arbitrage.monitor import settings
from bitcoin_arbitrage.monitor.log import setup_logger

from bitcoin_arbitrage.monitor.exchange import Exchange
from bitcoin_arbitrage.monitor.spread_detection import Spread
from bitcoin_arbitrage.monitor.update.notification import NotificationService

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
                try:
                    self._pb.push_note(title=f'Spread {spread.spread_with_currency}', body=f'{spread.summary}')
                except PushError as e:
                    logger.error(f'Cannot push spread via Pushbullet.\n{e}')
