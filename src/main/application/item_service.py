""" Use case: CRUD operations for the Item Entity """
from sqlalchemy.orm import Query
from ..domain.cart_item_entity import CartItem
from ..domain.cart_entity import Cart
from ..domain.item_entity import Item
from ..infrastructure.database.transaction import Transaction


class ItemService(object):
    """ Item Service class """

    async def create_item(self, code: str, name: str, price: float) -> None:
        """
        Creates a new item and inserts it to the database
        Args:
            name: item's name
            code: item's code
            price: item's price

        Returns: None

        """
        with Transaction() as t:
            t.session.add(Item(code=code, name=name, price=price))

    def read_item(self, filter_params: dict = None) -> Query:
        """
        Finds a item at the database according to the provided filters
        Args:
            filter_params: dict

        Returns: SQL Alchemy Query instance

        """
        with Transaction() as t:
            return t.session.query(Item).filter_by(**filter_params)

    async def read_items(self) -> Query:
        """
        Retrieves all items from the database
        Returns: SQL Alchemy Query instance

        """
        with Transaction() as t:
            return t.session.query(Item)

    def update_item(self, item_id: int, name: str = None, fullname: str = None, nickname: str = None) -> None:
        """
        Updates an existing item by id
        Args:
            item_id: Existing item's id
            name: item's new name
            fullname: item's new fullname
            nickname: item's new nickname

        Returns: None

        """
        raise NotImplementedError

    def delete_item(self, item_id: int) -> None:
        """
        Permanently removes a item from the database
        Args:
            item_id: Existing item's id

        Returns: None

        """
        raise NotImplementedError

    async def add_to_cart(self, item_id: int, cart_id: int):
        """
        Adds an item to a cart
        Args:
            item_id: Item's ID
            cart_id: Cart's ID

        Returns: None

        """
        with Transaction() as t:
            cart = t.session.query(Cart).filter_by(id=cart_id).first()
            item_to_cart = CartItem()
            item = t.session.query(Item).filter_by(id=item_id).first()
            item_to_cart.item = item
            cart.items.append(item_to_cart)

    async def remove_from_cart(self, item_id: int, cart_id: int):
        """
        Removes an item from a cart
        Args:
            item_id: Item's ID
            cart_id: Cart's ID

        Returns: None

        """
        with Transaction() as t:
            cart_item = \
                t.session.query(CartItem).filter_by(**{'carts_id': cart_id, 'items_id': item_id}).first()

            if cart_item:
                t.session.delete(cart_item)
