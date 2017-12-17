from enum import Enum


OrderId = str


class OrderStatus(Enum):
    PENDING = 'pending'
    DONE = 'done'
    CANCELLED = 'cancelled'


class Order:
    def __init__(self) -> None:
        from exchange import Exchange
        self.exchange: Exchange
        self.order_id: OrderId
        self.status: OrderStatus
