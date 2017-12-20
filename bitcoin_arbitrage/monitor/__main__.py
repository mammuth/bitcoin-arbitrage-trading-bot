import asyncio

from bitcoin_arbitrage.monitor.monitor import Monitor

# Direct entry to monitor for debugging purposes
if __name__ == '__main__':
    print('Starting monitor in debugging modus. You should run the flask app normally.')
    monitor_loop = asyncio.get_event_loop()
    monitor = Monitor()
    monitor_loop.run_until_complete(monitor.update())
