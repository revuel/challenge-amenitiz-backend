""" Transaction module """
from __future__ import annotations
from .setup import build_session
from ..logging.logger import LOGGER


class Transaction(object):
    """ Transaction Context Manager class. See "notes" to read a list of motivations behind implementing this class.
    Notes:
        - Effectively manage transactions: atomically or within a set of actions to be executed together
        - If all actions were successfully executed, the transaction is committed
        - If any action was unsuccessfully executed, the transaction is rolled back
        - The usage of slots is to avoid unnecessary dict overhead for this instances
    """

    __slots__ = ('session',)

    def __enter__(self) -> Transaction:
        """
        Initializes Transaction Context Manager
        Returns: Transaction

        """
        LOGGER.info(f'Initializing transaction')
        self.session = build_session()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb) -> None:
        """
        Auto close: Either commit or rollback this transaction
        Args:
            exc_type: Type of Exception caught in the context
            exc_val: Value of the Exception caught in the context
            exc_tb: Trace of the Exception caught in the context

        Returns: None

        """
        if exc_tb is exc_type is exc_val is None:
            try:
                self.session.commit()
                LOGGER.info(f'Transaction finished successfully!')
            except Exception as ex:
                LOGGER.error(f'Rolling back transaction due to a database exception: {ex}')
                self.session.rollback()
        else:
            LOGGER.error(f'Rolling back transaction due to an Exception: {exc_val}')
            self.session.rollback()
