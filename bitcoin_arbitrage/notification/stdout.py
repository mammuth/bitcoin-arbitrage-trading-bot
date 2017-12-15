import logging

import pushbullet as pb_lib

from notification import NotificationService
from spread_detection import Spread

logger = logging.Logger('Pushbullet')
logger.setLevel(logging.DEBUG)


class StdoutNotification(NotificationService):

    def notify(self, spread: Spread) -> bool:
        if super(StdoutNotification, self).notify(spread):
            # logger.info(spread.summary)
            print(spread.summary)
            return True
        return False
