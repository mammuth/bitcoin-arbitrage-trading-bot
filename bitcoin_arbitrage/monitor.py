import csv
import logging
from datetime import datetime
import asyncio
import os

import settings
from exchange import Exchange

logger = logging.getLogger('Monitor')


class Monitor:

    def __init__(self) -> None:
        self._update_task: asyncio.Task = None
        self._update_task_loop = None
        self._is_update_task_started = False
        if settings.UPDATE_INTERVAL < 5:
            raise ValueError('Please use an update interval >= 5 seconds')
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

    def notify(self) -> None:
        return NotImplemented

    async def _write_price_history_to_file(self, exchange: Exchange) -> None:
        # Write to file
        header = ['name', 'time_pretty', 'ask_price', 'bid_price', 'currency_pair', 'timestamp']
        timestamp = datetime.now().timestamp()
        row = {
            'timestamp': timestamp,
            'time_pretty': datetime.utcfromtimestamp(timestamp),
            'name': exchange.name,
            'ask_price': exchange.get_ask_price(),
            'bid_price': exchange.get_bid_price(),
            'currency_pair': exchange.currency_pair.value
        }
        # Create file if it does not yet exist
        if not os.path.isfile(settings.PRICE_HISTORY_FILE):
            f = open(settings.PRICE_HISTORY_FILE, 'w+')
            w = csv.DictWriter(f, header)
            w.writeheader()
            f.close()
        # Append data to file
        with open(settings.PRICE_HISTORY_FILE, 'a') as file:
            w = csv.DictWriter(file, header)
            w.writerow(row)

    async def _update(self) -> None:
        while True:
            for exchange in settings.EXCHANGES:
                logger.debug('Update...')
                await self._write_price_history_to_file(exchange)

            await asyncio.sleep(settings.UPDATE_INTERVAL)
