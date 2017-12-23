from enum import Enum

OrderId = str


class OrderState(Enum):
    PENDING = 'pending'
    DONE = 'done'
    CANCELLED = 'cancelled'


class Order:
    def __init__(self, exchange: 'Exchange', order_id: OrderId) -> None:
        self.exchange = exchange
        self.order_id = order_id
        self.state = OrderState.PENDING
