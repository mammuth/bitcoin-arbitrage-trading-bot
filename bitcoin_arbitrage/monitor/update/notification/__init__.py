from datetime import datetime

from abc import ABC, abstractmethod
from typing import List, Optional

from bitcoin_arbitrage.monitor.exchange import Exchange
from bitcoin_arbitrage.monitor.spread_detection import Spread
from bitcoin_arbitrage.monitor.update import UpdateAction


class NotificationService(UpdateAction, ABC):

    def __init__(self, spread_threshold: Optional[int] = None) -> None:
        super().__init__(spread_threshold)
        self._last_notification: datetime = None

    @abstractmethod
    def run(self, spreads: List[Spread], exchanges: List[Exchange], timestamp: float) -> None:
        raise NotImplementedError

    def _should_notify(self, time_between_notifications):
        now = datetime.now()

        if self._last_notification is None:
            self._last_notification = now
            return True

        seconds_since_last_notification = (now - self._last_notification).total_seconds()
        if seconds_since_last_notification >= time_between_notifications:
            self._last_notification = now
            return True

        return False

    def _get_spread_for_notification(self, spreads: List[Spread]) -> Optional[Spread]:
        spreads_above_threshold = [spread for spread in spreads if spread.spread > self.threshold]
        spreads_above_threshold.sort(key=lambda x: x.spread, reverse=True)
        return spreads_above_threshold[0] if spreads_above_threshold else None
