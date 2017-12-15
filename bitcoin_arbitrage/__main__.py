import logging
import sys

from bitcoin_arbitrage.monitor import Monitor

logger = logging.getLogger('main')
# logger.setLevel(settings.LOG_LEVEL)
logger.setLevel(logging.DEBUG)

ch = logging.StreamHandler(sys.stdout)
# ch.setLevel(settings.LOG_LEVEL)
ch.setLevel(logging.DEBUG)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
ch.setFormatter(formatter)
logging.root.addHandler(ch)

monitor = Monitor()
monitor.start()  # ToDo: This call should not be blocking