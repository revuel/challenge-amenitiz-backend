""" Utility to test rest controllers """
import unittest
from fastapi.testclient import TestClient
from src.main.presentation.rest.setup import app


class BaseRestTest(unittest.TestCase):
    """ Test utility class. For DRY purposes sets up a TestClient for every rest controller unit test """

    def setUp(self) -> None:
        self.rest_client = TestClient(app)

    def tearDown(self) -> None:
        """ Overridden method """
        pass
