import asyncio
import itertools
from datetime import datetime
from typing import List

import settings
from exchange import Exchange
from log import setup_logger
from spread_detection import Spread, SpreadMissingPriceError, SpreadDifferentCurrenciesError

logger = setup_logger('Monitor')


class Monitor:
    def __init__(self) -> None:
        self._update_task: asyncio.Task = None
        self._update_task_loop = None
        self._is_update_task_started = False
        self._last_spreads: List[Spread] = []
        self._update_interval = settings.UPDATE_INTERVAL

    def start(self) -> None:
        if not self._is_update_task_started:
            self._update_task = asyncio.Task(self._update())
            self._update_task_loop = asyncio.get_event_loop()
            self._update_task_loop.call_later(settings.UPDATE_INTERVAL, self.stop)

            try:
                self._update_task_loop.run_until_complete(self._update_task)
            except asyncio.CancelledError:
                pass

    def stop(self) -> None:
        if self._is_update_task_started:
            self._update_task.cancel()

    async def _update(self) -> None:
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
                spreads.append(spread)
            except SpreadMissingPriceError or SpreadDifferentCurrenciesError:
                pass
        return spreads
