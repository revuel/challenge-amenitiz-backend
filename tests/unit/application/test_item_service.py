""" Unit Test module for item_service module """
from src.main.application.item_service import ItemService
from src.main.application.prefill_service import Prefill
from tests.base_test import BaseTest


class TestItemService(BaseTest):
    """ Unit Test class for CartService class """

    @classmethod
    def setUpClass(cls) -> None:
        """ Overridden method. Puts a shared ItemService available for unit tests """
        cls.item_service = ItemService()

    async def test_create_item(self):
        """
        Checks that create item works
        Notes:
            - Arrange: N/A
            - Act: Create item
            - Assert: Item has been created
        Returns: None

        """
        test_item_data = {'code': 'TST', 'name': 'test_item', 'price': 4.2}

        await self.item_service.create_item(**test_item_data)

        item_query = self.item_service.read_item({'id': 1})
        actual_item = item_query.first()

        self.assertEqual(test_item_data['code'], actual_item.code)
        self.assertEqual(test_item_data['name'], actual_item.name)
        self.assertEqual(test_item_data['price'], actual_item.price)

    async def test_read_item(self):
        """
        Check that reading an item works
        Notes:
            - Arrange: Prefill items
            - Act: Read item by id
            - Assert: Item has been red
        Returns: None

        """
        await Prefill.items()

        item_query = self.item_service.read_item({'code': 'SR1'})
        actual_item = item_query.first()

        self.assertIsNot(None, actual_item)

    async def test_read_items(self):
        """
        Checks that reading multiple items works
        Notes:
            - Arrange: Prefill items
            - Act: Read items
            - Assert: Items can be red
        Returns: None

        """
        await Prefill.items()

        cart_query = await self.item_service.read_items()

        self.assertEqual(3, len(cart_query.all()))

    def test_update_item(self):
        """
        Checks that updating an item is not implemented yet
        Notes:
            - Arrange: N/A
            - Act: Update item
            - Assert: NotImplementedError is raised
        Returns: None

        """
        with self.assertRaises(NotImplementedError):
            self.item_service.update_item(0)

    def test_delete_item(self):
        """
        Checks that deleting an item is not implemented yet
        Notes:
            - Arrange: N/A
            - Act: Delete item
            - Assert: NotImplementedError is raised
        Returns: None

        """
        with self.assertRaises(NotImplementedError):
            self.item_service.delete_item(0)

    async def test_add_to_cart(self):
        """
        Checks that items can be added to carts
        Notes:
            - Arrange: Prefill users, carts and items
            - Act: Add items to cart
            - Assert: Items have been added to this particular cart
        Returns: None

        """
        await Prefill.users()
        await Prefill.carts()
        await Prefill.items()
        await self.item_service.add_to_cart(1, 1)
        await self.item_service.add_to_cart(2, 1)
        await self.item_service.add_to_cart(3, 1)

        item_query = await self.item_service.read_items()
        items = item_query.all()

        for item in items:
            self.assertEqual(1, item.carts[0].carts_id)

    async def test_remove_from_cart(self):
        """
        Checks that items can be removed from carts
        Notes:
            - Arrange: Prefill users, carts, items
            - Act: Remove item from cart
            - Assert: That item does not belong to the cart, while the rest are kept
        Returns: None

        """
        await Prefill.users()
        await Prefill.carts()
        await Prefill.items()
        await self.item_service.add_to_cart(1, 1)
        await self.item_service.add_to_cart(1, 1)
        await self.item_service.add_to_cart(1, 1)
        await self.item_service.remove_from_cart(1, 1)

        item_query = self.item_service.read_item({'id': 1})
        item = item_query.first()

        for cart_item in item.carts:
            self.assertFalse(cart_item.carts_id != 1)
