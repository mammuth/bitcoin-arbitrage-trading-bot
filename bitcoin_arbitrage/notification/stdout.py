import logging

import pushbullet as pb_lib

import settings
from log import setup_logger
from notification import NotificationService
from spread_detection import Spread

logger = setup_logger('Stdout')


class StdoutNotification(NotificationService):

    def notify(self, spread: Spread) -> bool:
        if super(StdoutNotification, self).notify(spread):
            # logger.info(spread.summary)
            print(spread.summary)
            return True
        return False
