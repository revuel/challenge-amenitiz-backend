""" Unit Test module for cart_service module """
from src.main.application.prefill_service import Prefill
from src.main.application.cart_service import CartService
from tests.base_test import BaseTest


class TestCartService(BaseTest):
    """ Unit Test class for CartService class """

    @classmethod
    def setUpClass(cls) -> None:
        """ Overridden method. Puts a shared CartService available for unit tests """
        cls.cart_service = CartService()

    async def test_create_cart(self):
        """
        Checks that create cart works
        Notes:
            - Arrange: Prefill user
            - Act: Create a cart (for that particular user)
            - Assert: Cart has been created
        Returns: None

        """
        await Prefill.users(1)
        await self.cart_service.create_cart(1)

        cart_query = await self.cart_service.read_carts()

        self.assertEqual(1, len(cart_query.all()))

    async def test_read_cart(self):
        """
        Checks that read cart works
        Notes:
            - Arrange: Prefill users and carts
            - Act: Read cart
            - Assert: Cart can be red
        Returns: None

        """
        await Prefill.users()
        await Prefill.carts()

        cart_query = await self.cart_service.read_cart({'id': 1})

        self.assertEqual(1, len(cart_query.all()))

    async def test_read_carts(self):
        """
        Checks that reading multiple carts works
        Notes:
            - Arrange: Prefill multiple users and carts
            - Act: Read carts
            - Assert: Carts can be red
        Returns: None

        """
        await Prefill.users()
        await Prefill.carts()

        cart_query = await self.cart_service.read_carts()

        self.assertEqual(10, len(cart_query.all()))

    def test_update_cart(self):
        """
        Checks that update cart is not implemented yet
        Notes:
            - Arrange: N/A
            - Act: Update cart
            - Assert: NotImplementedError is raised
        Returns: None

        """
        with self.assertRaises(NotImplementedError):
            self.cart_service.update_cart(0)

    def test_delete_cart(self):
        """
        Checks that delete cart is not implemented yet
        Notes:
            - Arrange: N/A
            - Act: Delete cart
            - Assert: NotImplementedError is raised
        Returns: None

        """
        with self.assertRaises(NotImplementedError):
            self.cart_service.delete_cart(0)
