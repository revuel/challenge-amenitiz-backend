""" Unit Test module for domain __init__ module """
from src.main.infrastructure.logging.logger import LOGGER
from src.main.domain.user_entity import User
from tests.base_test import BaseTest


class TestEntity(BaseTest):
    """ Unit Test class for Entity class """

    def test_enroll(self):
        """
        Checks enroll prints message
        Notes:
            - Arrange: N/A
            - Act: N/A
            - Assert: Entities' enroll method prints message
        Returns: None

        """
        with self.assertLogs(LOGGER, 'DEBUG') as cm:
            User.enroll()
            self.assertEqual('Enrolling User', cm.records[0].msg)
