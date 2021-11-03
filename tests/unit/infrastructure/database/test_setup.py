""" Unit Test module for database.setup module """
from sqlalchemy.engine import Engine

from src.main.infrastructure.database.setup import get_engine
from tests.base_test import BaseTest


class TestSetUp(BaseTest):
    """ Unit Test class for databse.setup module """

    def test_get_engine(self):
        """
        Checks that engine actually returns an Engine instance
        Notes:
            - Arrange: N/A
            - Act: N/A
            - Asserts: get_engine returns an Engine instance
        Returns: None

        """
        self.assertTrue(isinstance(get_engine(), Engine))
