from abc import ABC, abstractmethod
from typing import List, Optional

from exchange import Exchange
from spread_detection import Spread
from update import UpdateAction


class NotificationService(UpdateAction, ABC):
    @abstractmethod
    def run(self, spreads: List[Spread], exchanges: List[Exchange], timestamp: float) -> None:
        raise NotImplementedError

    def _get_spread_for_notification(self, spreads: List[Spread]) -> Optional[Spread]:
        spreads_above_threshold = [spread for spread in spreads if spread.spread > self.threshold]
        spreads_above_threshold.sort(key=lambda x: x.spread, reverse=True)
        return spreads_above_threshold[0] if spreads_above_threshold else None
