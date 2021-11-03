""" Database setup module """
from sqlalchemy import create_engine
from sqlalchemy.engine import Engine
from sqlalchemy.orm import sessionmaker, Session
from ..logging.logger import LOGGER
from ...domain import Base
from ...domain.cart_entity import Cart
from ...domain.cart_item_entity import CartItem
from ...domain.item_entity import Item
from ...domain.rule_entity import Rule
from ...domain.user_entity import User

# For the shake of simplicity, for the challenge purposes with an in-memory SQLite should be enough
engine = create_engine('sqlite:///:memory:', echo=True, connect_args={"check_same_thread": False})


def init_db() -> None:
    """
    Initializes database from domain model
    Returns: None

    """
    LOGGER.info(f'Initializing domain model')
    CartItem.enroll()
    User.enroll()
    Item.enroll()
    Cart.enroll()
    Rule.enroll()
    Base.metadata.create_all(engine)


def shutdown_db() -> None:
    """
    Cleans up database model
    Returns: None

    """
    Base.metadata.drop_all(engine)


def get_engine() -> Engine:
    """
    Obtain a reference to the current database running engine
    Returns: Engine

    """
    return engine


def build_session() -> Session:
    """
    Creates and returns new SQL Alchemy Session
    Returns: Session

    """
    _session = sessionmaker(bind=engine)
    _session.configure(bind=engine)
    return _session()
