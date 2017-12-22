from enum import Enum

from bitcoin_arbitrage.monitor.exchange import Exchange

OrderId = str


class OrderStatus(Enum):
    PENDING = 'pending'
    DONE = 'done'
    CANCELLED = 'cancelled'


class Order:
    def __init__(self, exchange: Exchange, order_id: OrderId) -> None:
        self.exchange = exchange
        self.order_id = order_id
        self.status = OrderStatus.PENDING
