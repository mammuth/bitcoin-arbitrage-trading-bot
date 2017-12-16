from datetime import datetime

from abc import ABC, abstractmethod
from typing import List, Optional

import settings
from exchange import Exchange
from spread_detection import Spread
from update import UpdateAction


class NotificationService(UpdateAction, ABC):

    def __init__(self, spread_threshold: Optional[int] = None) -> None:
        super().__init__(spread_threshold)
        self.last_notification: datetime = None

    @abstractmethod
    def run(self, spreads: List[Spread], exchanges: List[Exchange], timestamp: float) -> None:
        raise NotImplementedError

    def _should_notify(self):
        if self.last_notification is None:
            return True
        now = datetime.now()
        seconds_since_last_notification = (now - self.last_notification).total_seconds()
        if seconds_since_last_notification >= settings.TIME_BETWEEN_NOTIFICATIONS:
            self.last_notification = now
            return True
        return False

    def _get_spread_for_notification(self, spreads: List[Spread]) -> Optional[Spread]:
        spreads_above_threshold = [spread for spread in spreads if spread.spread > self.threshold]
        spreads_above_threshold.sort(key=lambda x: x.spread, reverse=True)
        return spreads_above_threshold[0] if spreads_above_threshold else None
