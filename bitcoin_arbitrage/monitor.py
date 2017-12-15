import csv
import logging
from datetime import datetime
import asyncio
import os
from typing import List

import itertools

import settings
from exchange import Exchange
from spread_detection import Spread

logger = logging.getLogger('Monitor')
logger.setLevel(logging.DEBUG)


class Monitor:

    def __init__(self) -> None:
        self._update_task: asyncio.Task = None
        self._update_task_loop = None
        self._is_update_task_started = False
        self._last_spreads: List[Spread] = []

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

    async def _update(self) -> None:
        while True:
            logger.debug('Update...')
            for exchange in settings.EXCHANGES:
                exchange.update_prices()
                # await self._write_price_history_to_file(exchange)

            self._last_spreads = self._calculate_spreads()
            for spread in self._last_spreads:
                if spread.is_above_trading_thresehold():
                    logger.debug(f'Spread above trading threshold: {spread}')
                    # ToDo Write into file
                    # ToDo Somehow wire to a trading component
                    pass
                for service in settings.NOTIFICATION_SERVICES:
                    service.notify(spread=spread)
                if spread.spread > settings.SPREAD_HISTORY_THRESHOLD:
                    await self._write_spread_to_file(spread)
            await asyncio.sleep(settings.UPDATE_INTERVAL)

    def _calculate_spreads(self) -> List[Spread]:
        combinations: List[(Exchange, Exchange)] = itertools.combinations(settings.EXCHANGES, 2)
        return [Spread(exchange_one=pair[0], exchange_two=pair[1]) for pair in combinations]

    async def _write_spread_to_file(self, spread: Spread) -> None:
        # Write to file
        header = ['buy_exchange', 'sell_exchange', 'spread', 'time_pretty', 'buy_price', 'sell_price', 'currency_pair',
                  'timestamp']
        filename = settings.SPREAD_HISTORY_FILE
        timestamp = datetime.now().timestamp()
        row = {
            'buy_exchange': spread.exchange_buy,
            'sell_exchange': spread.exchange_sell,
            'spread': spread.spread,
            'time_pretty': datetime.utcfromtimestamp(timestamp),
            'buy_price': spread.exchange_buy.last_ask_price,
            'sell_price': spread.exchange_sell.last_bid_price,
            'currency_pair': spread.exchange_buy.currency_pair.value,
            'timestamp': timestamp,
        }
        # Create file if it does not yet exist
        if not os.path.isfile(filename):
            f = open(filename, 'w+')
            w = csv.DictWriter(f, header)
            w.writeheader()
            f.close()
        # Append data to file
        with open(filename, 'a') as file:
            w = csv.DictWriter(file, header)
            w.writerow(row)

    async def _write_price_history_to_file(self, exchange: Exchange) -> None:
        # Write to file
        header = ['name', 'time_pretty', 'ask_price', 'bid_price', 'currency_pair', 'timestamp']
        filename = settings.PRICE_HISTORY_FILE
        timestamp = datetime.now().timestamp()
        row = {
            'timestamp': timestamp,
            'time_pretty': datetime.utcfromtimestamp(timestamp),
            'name': exchange.name,
            'ask_price': exchange.last_ask_price,
            'bid_price': exchange.last_bid_price,
            'currency_pair': exchange.currency_pair.value
        }
        # Create file if it does not yet exist
        if not os.path.isfile(filename):
            f = open(filename, 'w+')
            w = csv.DictWriter(f, header)
            w.writeheader()
            f.close()
        # Append data to file
        with open(filename, 'a') as file:
            w = csv.DictWriter(file, header)
            w.writerow(row)
