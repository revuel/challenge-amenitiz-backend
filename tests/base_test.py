""" Base Test class to aid database refresh on Unit Tests"""
import aiounittest

from src.main.infrastructure.database.setup import init_db, shutdown_db


class BaseTest(aiounittest.AsyncTestCase):
    """ Test utility class. For DRY purposes, init and clean up DB before and after each unit test """

    def setUp(self) -> None:
        """ Initializes DB """
        init_db()

    def tearDown(self) -> None:
        """ Destroys DB """
        shutdown_db()
