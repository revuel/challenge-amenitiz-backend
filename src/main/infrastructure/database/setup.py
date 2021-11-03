""" Database setup module """
from sqlalchemy import create_engine
from sqlalchemy.engine import Engine
from sqlalchemy.orm import sessionmaker, Session
from ..logging.logger import LOGGER
from ...domain import Base

# For the shake of simplicity, for the challenge purposes with an in-memory SQLite should be enough
engine = create_engine('sqlite:///:memory:', echo=True, connect_args={"check_same_thread": False})


def init_db() -> None:
    """
    Initializes database model
    Returns: None

    """
    LOGGER.info(f'Initializing domain model')

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
