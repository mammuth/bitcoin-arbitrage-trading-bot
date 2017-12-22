from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.sql import func
from bitcoin_arbitrage.app import db
from bitcoin_arbitrage.config import SQLALCHEMY_DATABASE_URI
from bitcoin_arbitrage.monitor.currency import CurrencyPair

engine = create_engine(SQLALCHEMY_DATABASE_URI, echo=True)
db_session = scoped_session(sessionmaker(autocommit=False,
                                         autoflush=False,
                                         bind=engine))
Base = declarative_base()
Base.query = db_session.query_property()

# create all tables
Base.metadata.create_all(bind=engine)


class Spread(db.Model):
    __tablename__ = 'spread'

    id = db.Column(db.Integer, primary_key=True)
    recorded_date = db.Column(db.DateTime(timezone=True), server_default=func.now())

    spread = db.Column(db.Integer)

    exchange_buy_id = db.Column(db.Integer, db.ForeignKey('exchange.id'))
    exchange_sell_id = db.Column(db.Integer, db.ForeignKey('exchange.id'))

    exchange_buy = db.relationship('Exchange', foreign_keys=[exchange_buy_id])
    exchange_sell = db.relationship('Exchange', foreign_keys=[exchange_sell_id])


class Exchange(db.Model):
    __tablename__ = 'exchange'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), nullable=False)
    currency_pair = db.Column(db.Enum(CurrencyPair))
    last_ask_price = db.Column(db.Integer)
    last_bid_price = db.Column(db.Integer)
