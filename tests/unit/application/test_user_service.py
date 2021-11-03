""" Unit Test module for user_service module """
from src.main.application.prefill_service import Prefill
from src.main.application.user_service import UserService
from tests.base_test import BaseTest


class TestUserService(BaseTest):
    """ Unit Test class for UserService class """

    @classmethod
    def setUpClass(cls) -> None:
        """ Overridden method. Puts a shared UserService available for unit tests """
        cls.user_service = UserService()

    async def test_create_user(self):
        """
        Checks user creation works
        Notes:
            - Arrange: N/A
            - Act: Fake user is created
            - Assert: Fake user exists (has been committed)
        Returns: None

        """
        user_data = {'name': 'name', 'fullname': 'fullname', 'nickname': 'nickname'}
        self.user_service.create_user(**user_data)
        user_query = self.user_service.read_user({'id': 1})
        actual_user = user_query.first()

        self.assertEqual(actual_user.name, user_data['name'])
        self.assertEqual(actual_user.fullname, user_data['fullname'])
        self.assertEqual(actual_user.nickname, user_data['nickname'])

    async def test_read_user(self):
        """
        Checks user read works
        Notes:
            - Arrange: Prefill one user
            - Act: Read user by id
            - Assert: User exists
        Returns: None

        """
        await Prefill.users(1)

        user_query = self.user_service.read_user({'id': 1})

        self.assertEqual(1, user_query.count())

    async def test_read_users(self):
        """
        Checks user read multiple users works
        Notes:
            - Arrange: Prefill multiple users
            - Act: Read multiple users
            - Assert: Multiple users are red
        Returns: None

        """
        await Prefill.users(11)

        user_query = await self.user_service.read_users()

        self.assertEqual(11, user_query.count())

    def test_update_user(self):
        """
        Checks update user is not implemented yet
        Notes:
            - Arrange: N/A
            - Act: Update user
            - Assert: NotImplementedError is raised
        Returns: None

        """
        with self.assertRaises(NotImplementedError):
            self.user_service.update_user(0)

    def test_delete_user(self):
        """
        Checks update user is not implemented yet
        Notes:
            - Arrange: N/A
            - Act: Delete user
            - Assert: NotImplementedError is raised
        Returns: None

        """
        with self.assertRaises(NotImplementedError):
            self.user_service.delete_user(0)
