from abc import ABC, abstractmethod
from typing import List, Optional

from bitcoin_arbitrage.monitor import settings
from bitcoin_arbitrage import app
from bitcoin_arbitrage.app import app, db

from bitcoin_arbitrage.monitor.exchange import Exchange


class UpdateAction(ABC):
    from bitcoin_arbitrage.models import Spread
    def __init__(self, spread_threshold: Optional[int]=None) -> None:
        self.threshold = spread_threshold or 0

    @abstractmethod
    def run(self, spreads: List[Spread], exchanges: List[Exchange], timestamp: float) -> None:
        raise NotImplementedError
