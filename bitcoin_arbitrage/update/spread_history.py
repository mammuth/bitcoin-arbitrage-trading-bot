import csv
from datetime import datetime
from typing import List

import os

import settings
from exchange import Exchange
from spread_detection import Spread
from update import UpdateAction


class SpreadHistory(UpdateAction):
    def run(self, spreads: List[Spread], exchanges: List[Exchange], timestamp: float) -> None:
        header = ['buy_exchange', 'sell_exchange', 'spread', 'time_pretty', 'buy_price', 'sell_price', 'currency_pair',
                  'timestamp']
        filename = settings.SPREAD_HISTORY_FILE

        # Create file if it does not yet exist
        if not os.path.isfile(filename):
            f = open(filename, 'w+')
            w = csv.DictWriter(f, header)
            w.writeheader()
            f.close()

        for spread in spreads:
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
            # Append data to file
            with open(filename, 'a') as file:
                w = csv.DictWriter(file, header)
                w.writerow(row)
