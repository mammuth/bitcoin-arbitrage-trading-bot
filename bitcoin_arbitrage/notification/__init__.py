from abc import ABC, abstractmethod
from spread_detection import Spread


class NotificationService(ABC):

    def __init__(self, spread_threshold: float) -> None:
        self.threshold = spread_threshold

    def notify(self, spread: Spread) -> bool:
        return spread.spread > self.threshold
