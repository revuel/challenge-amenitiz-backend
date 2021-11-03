""" Use case: CRUD operations for the Cart Entity """
from sqlalchemy.orm import Query
from ..domain.cart_entity import Cart
from ..infrastructure.database.transaction import Transaction


class CartService(object):
    """ Cart Service class """

    async def create_cart(self, user_id) -> None:
        """
        Creates a new cart and inserts it to the database
        Args:
            user_id: User's ID

        Returns: None

        """
        with Transaction() as t:
            t.session.add(Cart(user_id=user_id))

    async def read_cart(self, filter_params: dict = None) -> Query:
        """
        Finds a cart at the database according to the provided filters
        Args:
            filter_params: dict

        Returns: SQL Alchemy Query instance

        """
        with Transaction() as t:
            return t.session.query(Cart).filter_by(**filter_params)

    async def read_carts(self) -> Query:
        """
        Retrieves all carts from the database
        Returns: SQL Alchemy Query instance

        """
        with Transaction() as t:
            return t.session.query(Cart)

    def update_cart(self, cart_id: int, total_price: int = 0) -> None:
        """
        Updates an existing cart by id
        Args:
            cart_id: Existing cart's id
            total_price: Cart's total price

        Returns: None

        """
        raise NotImplementedError

    def delete_cart(self, cart_id: int) -> None:
        """
        Permanently removes a cart from the database
        Args:
            cart_id: Existing cart's id

        Returns: None

        """
        raise NotImplementedError
