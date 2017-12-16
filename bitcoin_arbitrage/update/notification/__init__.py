from abc import ABC, abstractmethod
from typing import List

from exchange import Exchange
from spread_detection import Spread
from update import UpdateAction


class NotificationService(UpdateAction, ABC):
    @abstractmethod
    def run(self, spreads: List[Spread], exchanges: List[Exchange], timestamp: float) -> None:
        raise NotImplementedError

    def _should_notify(self, spread: Spread) -> bool:
        return spread.spread > self.threshold
