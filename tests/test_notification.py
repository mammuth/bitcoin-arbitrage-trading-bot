from datetime import datetime

from update.notification.stdout import StdoutNotification


def test_should_notify():
    notification = StdoutNotification()
    assert notification._should_notify(5) is True
    assert notification._should_notify(5) is False
    notification._last_notification = datetime.now() - datetime.fromtimestamp(5)
    assert notification._should_notify(5) is True
