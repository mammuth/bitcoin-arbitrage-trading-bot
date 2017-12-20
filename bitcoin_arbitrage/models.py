from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.sql import func
from bitcoin_arbitrage.app import db
from bitcoin_arbitrage.config import SQLALCHEMY_DATABASE_URI
from bitcoin_arbitrage.monitor import settings
from bitcoin_arbitrage.monitor.currency_pair import CurrencyPair

from bitcoin_arbitrage.monitor.exchange import Exchange

engine = create_engine(SQLALCHEMY_DATABASE_URI, echo=True)
db_session = scoped_session(sessionmaker(autocommit=False,
                                         autoflush=False,
                                         bind=engine))
Base = declarative_base()
Base.query = db_session.query_property()

# create all tables
Base.metadata.create_all(bind=engine)


class SpreadDifferentCurrenciesError(Exception):
    pass


class SpreadMissingPriceError(Exception):
    pass


class Spread(db.Model):
    __tablename__ = 'spread'

    column_id = db.Column(db.Integer, primary_key=True)
    column_recorded_date = db.Column(db.DateTime(timezone=True), server_default=func.now())

    column_spread = db.Column(db.Integer)

    column_exchange_buy_id = db.Column(db.Integer, db.ForeignKey('exchange.id'))
    column_exchange_sell_id = db.Column(db.Integer, db.ForeignKey('exchange.id'))

    column_exchange_buy = db.relationship('Exchange', foreign_keys=[column_exchange_buy_id])
    column_exchange_sell = db.relationship('Exchange', foreign_keys=[column_exchange_sell_id])

    def __init__(self, exchange_one: Exchange, exchange_two: Exchange) -> None:
        super(Spread, self).__init__()
        if exchange_one.currency_pair != exchange_two.currency_pair:
            # logger.warning('Spread between different currency pairs is not supported')
            raise SpreadDifferentCurrenciesError('Spread between different currency pairs is not supported')
        self.exchange_one = exchange_one
        self.exchange_two = exchange_two
        self.exchange_buy: Exchange = None
        self.exchange_sell: Exchange = None
        self.spread = self._calculate_spread()

    def __str__(self) -> str:
        return self.summary

    def __repr__(self) -> str:
        return self.__str__()

    @property
    def summary(self) -> str:
        return f'{self.exchange_buy} [{self.exchange_buy.last_ask_price}] -> ' \
               f'{self.exchange_sell} [{self.exchange_sell.last_bid_price}] -> ' \
               f'Spread: {self.spread_with_currency}'

    @property
    def spread_with_currency(self) -> str:
        return f'{self.spread} {self.exchange_buy.currency_pair.fiat_symbol}'

    @property
    def spread_percentage(self):
        return self.spread / self.exchange_buy.last_bid_price

    def _calculate_spread(self) -> int:
        # if any of the necessary values is unavailale, a spread can not be calculated
        if None in [self.exchange_one.last_bid_price, self.exchange_one.last_ask_price,
                    self.exchange_two.last_bid_price, self.exchange_two.last_ask_price]:
            # logger.warning('Cannot calculate this spread because one of the prices is missing.')
            raise SpreadMissingPriceError('Cannot calculate this spread because one of the prices is missing.')

        d1 = int(self.exchange_one.last_bid_price - self.exchange_two.last_ask_price)
        d2 = int(self.exchange_two.last_bid_price - self.exchange_one.last_ask_price)

        if d1 > d2:
            self.exchange_buy = self.exchange_two
            self.exchange_sell = self.exchange_one
            return d1
        else:
            self.exchange_buy = self.exchange_one
            self.exchange_sell = self.exchange_two
            return d2

    def is_above_trading_thresehold(self) -> bool:
        return self.spread > settings.MINIMUM_SPREAD_TRADING


# ToDo: Merge monitor.exchange in
class Exchange(db.Model):
    __tablename__ = 'exchange'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), nullable=False)
    currency_pair = db.Column(db.Enum(CurrencyPair))
    last_ask_price = db.Column(db.Integer)
    last_bid_price = db.Column(db.Integer)
