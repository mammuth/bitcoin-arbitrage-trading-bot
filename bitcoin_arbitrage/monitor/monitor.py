import asyncio
import itertools
from datetime import datetime
from typing import List

from bitcoin_arbitrage.monitor import settings
from bitcoin_arbitrage.monitor.exchange import Exchange
from bitcoin_arbitrage.monitor.log import setup_logger
from bitcoin_arbitrage.monitor.spread_detection import Spread, SpreadMissingPriceError, SpreadDifferentCurrenciesError

logger = setup_logger('Monitor')


class Monitor:
    def __init__(self) -> None:
        self._last_spreads: List[Spread] = []

    async def update(self) -> None:
        while True:
            logger.debug('Update...')

            for exchange in settings.EXCHANGES:
                exchange.update_prices()

            spreads = self._calculate_spreads()
            timestamp = datetime.now().timestamp()

            for action in settings.UPDATE_ACTIONS:
                action.run(spreads, settings.EXCHANGES, timestamp)  # ToDo: Run every action asynchronously?

            await asyncio.sleep(settings.UPDATE_INTERVAL)

    def _calculate_spreads(self) -> List[Spread]:
        combinations: List[(Exchange, Exchange)] = itertools.combinations(settings.EXCHANGES, 2)
        spreads: List[Spread] = []
        for pair in combinations:
            try:
                spread = Spread(exchange_one=pair[0], exchange_two=pair[1])
                if spread.spread > 0:
                    spreads.append(spread)
            except (SpreadMissingPriceError, SpreadDifferentCurrenciesError):
                pass
        return spreads
