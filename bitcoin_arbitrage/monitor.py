import settings


class Monitor:
    @classmethod
    def update(cls):
        # ToDo: Automatically periodically run this
        for exchange in settings.EXCHANGES:
            print(exchange)

    @classmethod
    def notify(cls):
        return NotImplemented
