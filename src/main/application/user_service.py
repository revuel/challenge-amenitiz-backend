""" Use case: CRUD operations for the User Entity """
from sqlalchemy.orm import Query

from ..domain.user_entity import User
from ..infrastructure.database.transaction import Transaction


class UserService(object):
    """ User Service class """

    def create_user(self, name: str, fullname: str, nickname: str) -> None:
        """
        Creates a new User and inserts it to the database
        Args:
            name: User's name
            fullname: User's fullname
            nickname: User's alias

        Returns: None

        """
        with Transaction() as t:
            t.session.add(User(name=name, fullname=fullname, nickname=nickname))

    def read_user(self, filter_params: dict = None) -> Query:
        """
        Finds a user at the database according to the provided filters
        Args:
            filter_params: dict

        Returns: SQL Alchemy Query instance

        """
        with Transaction() as t:
            return t.session.query(User).filter_by(**filter_params)

    async def read_users(self) -> Query:
        """
        Retrieves all users from the database
        Returns: SQL Alchemy Query instance

        """
        with Transaction() as t:
            return t.session.query(User)

    def update_user(self, user_id: int, name: str = None, fullname: str = None, nickname: str = None) -> None:
        """
        Updates an existing user by id
        Args:
            user_id: Existing User's id
            name: User's new name
            fullname: User's new fullname
            nickname: User's new nickname

        Returns: None

        """
        raise NotImplementedError

    def delete_user(self, user_id: int) -> None:
        """
        Permanently removes a user from the database
        Args:
            user_id: Existing User's id

        Returns: None

        """
        raise NotImplementedError
