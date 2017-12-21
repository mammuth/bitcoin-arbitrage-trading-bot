from datetime import datetime, timedelta

from bitcoin_arbitrage.monitor import settings  # NOQA
from bitcoin_arbitrage.monitor.update.notification.stdout import StdoutNotification


def test_should_notify():
    notification = StdoutNotification()
    assert notification._should_notify(5) is True
    assert notification._should_notify(5) is False
    notification._last_notification = datetime.now() - timedelta(seconds=5)
    assert notification._should_notify(5) is True
