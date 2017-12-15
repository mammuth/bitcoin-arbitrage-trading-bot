from abc import ABC, abstractmethod

from bitcoin_arbitrage.spread_detection import Spread


class NotificationService(ABC):

    @abstractmethod
    def notify(self, spread: Spread) -> None:
        raise NotImplementedError
