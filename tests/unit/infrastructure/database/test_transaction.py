""" Unit Test module for transaction module """
from unittest.mock import MagicMock, Mock

from src.main.infrastructure.database.transaction import Transaction
from tests.base_test import BaseTest


class TestTransaction(BaseTest):
    """ Unit Test class for Transaction class """

    def test_transaction_commits(self):
        """
        Checks transaction actually finishes committing session
        Notes:
            - Arrange: N/A
            - Act: N/A
            - Asserts: session is not rolled back when everything goes fine
        Returns: None

        """
        with Transaction() as t:
            mock_rollback = MagicMock()
            mock_commit = MagicMock()
            setattr(t.session, 'commit', mock_commit)
            setattr(t.session, 'rollback', mock_rollback)

        self.assertFalse(mock_rollback.called)

    def test_transaction_rollsback(self):
        """
        Checks transaction rolls back if any Exception is raised inside the context manager
        Notes:
            - Arrange: N/A
            - Act: N/A
            - Asserts: session is rolled back when everything exception occurs
        Returns: None

        """

        with Transaction() as t:
            mock_rollback = MagicMock()
            mock_commit = MagicMock()
            mock_commit.side_effect = Mock(side_effect=Exception('Testing rollback'))
            setattr(t.session, 'commit', mock_commit)
            setattr(t.session, 'rollback', mock_rollback)

        self.assertTrue(mock_rollback.called)
