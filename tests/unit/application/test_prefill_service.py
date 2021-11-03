""" Unit Test module for prefill_service module """
from src.main.application.cart_service import CartService
from src.main.application.rules_service import RuleService
from src.main.application.item_service import ItemService
from src.main.application.prefill_service import Prefill
from src.main.application.user_service import UserService
from tests.base_test import BaseTest


class TestPrefill(BaseTest):
    """ Unit Test class for PrefillService class """

    @classmethod
    def setUpClass(cls) -> None:
        cls.user_service = UserService()
        cls.item_service = ItemService()
        cls.rule_service = RuleService()
        cls.cart_service = CartService()

    async def test_users(self):
        await Prefill.users(5)

        users_query = await self.user_service.read_users()

        self.assertEqual(5, len(users_query.all()))

    async def test_items(self):
        await Prefill.items()

        items_query = await self.item_service.read_items()

        self.assertEqual(3, len(items_query.all()))

    async def test_rules(self):
        await Prefill.rules()

        rules_query = await self.rule_service.read_offer_rules()

        self.assertEqual(3, len(rules_query.all()))

    async def test_carts(self):
        await Prefill.users(3)
        await Prefill.carts()

        carts_query = await self.cart_service.read_carts()

        self.assertEqual(3, len(carts_query.all()))

    async def test_all(self):
        await Prefill.all()

        users_query = await self.user_service.read_users()
        items_query = await self.item_service.read_items()
        rules_query = await self.rule_service.read_offer_rules()
        carts_query = await self.cart_service.read_carts()

        self.assertEqual(10, len(users_query.all()))
        self.assertEqual(3, len(items_query.all()))
        self.assertEqual(3, len(rules_query.all()))
        self.assertEqual(10, len(carts_query.all()))
