import csv
from datetime import datetime
from typing import List, Optional

import os

from bitcoin_arbitrage.monitor.exchange import Exchange
from bitcoin_arbitrage.monitor.update import UpdateAction


class AbstractSpreadToCSV(UpdateAction):
    from bitcoin_arbitrage.monitor.spread_detection import Spread

    def __init__(self, filename: str, should_override: bool, spread_threshold: Optional[int] = None) -> None:
        super().__init__(spread_threshold)
        self.header = ['buy_exchange', 'sell_exchange', 'spread', 'time_pretty', 'buy_price', 'sell_price',
                       'currency_pair', 'timestamp']
        self.filename = filename
        self.should_override = should_override

    def run(self, spreads: List[Spread], exchanges: List[Exchange], timestamp: float) -> None:
        # Create file if it does not yet exist
        if not os.path.isfile(self.filename):
            f = open(self.filename, 'w+')
            w = csv.DictWriter(f, self.header)
            w.writeheader()
            f.close()

        rows: List[dict] = []
        for spread in spreads:
            if None in [spread.exchange_buy, spread.exchange_sell]:
                continue
            row = {
                'buy_exchange': spread.exchange_buy.name,
                'sell_exchange': spread.exchange_sell.name,
                'spread': spread.spread,
                'time_pretty': datetime.utcfromtimestamp(timestamp),
                'buy_price': spread.exchange_buy.last_ask_price,
                'sell_price': spread.exchange_sell.last_bid_price,
                'currency_pair': spread.exchange_buy.currency_pair.value,
                'timestamp': timestamp,
            }
            rows.append(row)

        if self.should_override:
            with open(self.filename, 'w') as file:
                w = csv.DictWriter(file, self.header)
                w.writeheader()
                w.writerows(rows)
        else:
            # Append data to file
            with open(self.filename, 'a') as file:
                w = csv.DictWriter(file, self.header)
                w.writerows(rows)


class LastSpreadsToCSV(AbstractSpreadToCSV):
    def __init__(self, filename: str, should_override=True, spread_threshold: Optional[int] = None) -> None:
        super().__init__(filename, should_override, spread_threshold)


class SpreadHistoryToCSV(AbstractSpreadToCSV):
    def __init__(self, filename: str, should_override=False, spread_threshold: Optional[int] = None) -> None:
        super().__init__(filename, should_override, spread_threshold)
