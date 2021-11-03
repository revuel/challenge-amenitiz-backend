""" Unit Test module for rule_service module """
import random

from src.main.application.cart_service import CartService
from src.main.application.item_service import ItemService
from src.main.application.user_service import UserService
from src.main.domain.rule_entity import Rule
from src.main.domain.item_entity import Item
from src.main.application.rules_service import RuleService, RuleEngine
from src.main.application.prefill_service import Prefill
from tests.base_test import BaseTest

TEST_RULE = {
    'item_code': 'M22',
    'name': 'buy-one-get-one-free',
    'description': f'Just Miguel doing some tests: Buy 10 or more, each item at half price!',
    'firing_condition_operator': '>=',
    'firing_condition_quantity': 10,
    'effect_type': 'update_prices',
    'effect_percentage': 0.5,
}


class TestRuleService(BaseTest):
    """ Unit Test class for RuleService class """

    @classmethod
    def setUpClass(cls) -> None:
        """ Overridden method. Puts a shared RuleService available for unit tests """
        cls.rule_service = RuleService()

    def test_create_offer_rule(self):
        """
        Notes:
            - Arrange:
            - Act:
            - Assert:
        Returns: None

        """
        self.rule_service.create_offer_rule(**TEST_RULE)

        rule_query = self.rule_service.read_offer_rule({'id': 1})
        actual_rule = rule_query.first()

        self.assertEqual(1, rule_query.count())
        self.assertEqual(TEST_RULE['item_code'], actual_rule.item_code)
        self.assertEqual(TEST_RULE['name'], actual_rule.name)
        self.assertEqual(TEST_RULE['description'], actual_rule.description)
        self.assertEqual(TEST_RULE['firing_condition_operator'], actual_rule.firing_condition_operator)
        self.assertEqual(TEST_RULE['firing_condition_quantity'], actual_rule.firing_condition_quantity)
        self.assertEqual(TEST_RULE['effect_type'], actual_rule.effect_type)
        self.assertEqual(TEST_RULE['effect_percentage'], actual_rule.effect_percentage)

    async def test_read_offer_rule(self):
        """
        Notes:
            - Arrange:
            - Act:
            - Assert:
        Returns: None

        """
        await Prefill.rules()

        rule_query = self.rule_service.read_offer_rule({'item_code': 'GR1'})
        rule = rule_query.first()

        self.assertEqual(1, rule_query.count())
        self.assertEqual('GR1', rule.item_code)

    async def test_read_offer_rules(self):
        """
        Notes:
            - Arrange:
            - Act:
            - Assert:
        Returns: None

        """
        await Prefill.rules()

        rule_query = await self.rule_service.read_offer_rules()

        self.assertEqual(3, rule_query.count())

    def test_update_offer_rule(self):
        """
        Notes:
            - Arrange:
            - Act:
            - Assert:
        Returns: None

        """
        with self.assertRaises(NotImplementedError):
            self.rule_service.update_offer_rule(0)

    def test_delete_rule(self):
        """
        Notes:
            - Arrange:
            - Act:
            - Assert:
        Returns: None

        """
        with self.assertRaises(NotImplementedError):
            self.rule_service.delete_rule(0)


class TestRuleEngine(BaseTest):

    @classmethod
    def setUpClass(cls) -> None:
        """ Overridden method. Puts a shared RuleEngine, RuleService, UserService, CartService and ItemService available
         for unit tests """
        cls.rule_engine = RuleEngine()
        cls.rule_service = RuleService()
        cls.user_service = UserService()
        cls.cart_service = CartService()
        cls.item_service = ItemService()

    async def test_apply_challenge_sample_1(self):
        """
        Checks that challenge first sample works as expected
        Notes:
            - Arrange: Create a cart with 3 green tea, one strawberries and one coffee
            - Act: Invoke apply
            - Assert: Total Cart price is 22.45
        Returns: None

        """
        await Prefill.rules()
        await Prefill.items()
        await Prefill.users(1)
        await Prefill.carts()

        # 1 2 1 1 3 | GR1,SR1,GR1,GR1,CF1 -> 22.45€
        await self.item_service.add_to_cart(1, 1)
        await self.item_service.add_to_cart(2, 1)
        await self.item_service.add_to_cart(1, 1)
        await self.item_service.add_to_cart(1, 1)
        await self.item_service.add_to_cart(3, 1)

        await self.rule_engine.apply(1)

        cart_query = await self.cart_service.read_cart({'id': 1})
        actual_cart = cart_query.first()

        self.assertEqual(22.45, actual_cart.total_price)

    async def test_apply_challenge_sample_2(self):
        """
        Checks that challenge second sample works as expected
        Notes:
            - Arrange: Create a cart two strawberries
            - Act: Invoke apply
            - Assert: Total Cart price is 3.11
        Returns: None

        """
        await Prefill.rules()
        await Prefill.items()
        await Prefill.users(1)
        await Prefill.carts()

        # 1 1 | GR1,GR1 -> 3.11€
        await self.item_service.add_to_cart(1, 1)
        await self.item_service.add_to_cart(1, 1)

        await self.rule_engine.apply(1)

        cart_query = await self.cart_service.read_cart({'id': 1})
        actual_cart = cart_query.first()

        self.assertEqual(3.11, actual_cart.total_price)

    async def test_apply_challenge_sample_3(self):
        """
        Checks that challenge third sample works as expected
        Notes:
            - Arrange: Create a cart with one green tea and two strawberries
            - Act: Invoke apply
            - Assert: Total Cart price is 16.61
        Returns: None

        """
        await Prefill.rules()
        await Prefill.items()
        await Prefill.users(1)
        await Prefill.carts()

        # 2 2 1 2 | SR1,SR1,GR1,SR1 -> 16.61€
        await self.item_service.add_to_cart(2, 1)
        await self.item_service.add_to_cart(2, 1)
        await self.item_service.add_to_cart(1, 1)
        await self.item_service.add_to_cart(2, 1)

        await self.rule_engine.apply(1)

        cart_query = await self.cart_service.read_cart({'id': 1})
        actual_cart = cart_query.first()

        self.assertEqual(16.61, actual_cart.total_price)

    async def test_apply_challenge_sample_4(self):
        """
        Checks that challenge fourth sample works as expected
        Notes:
            - Arrange: Create a cart with one green tea, one strawberries and three coffees
            - Act: Invoke apply
            - Assert: Total Cart price is 30.57
        Returns: None

        """
        await Prefill.rules()
        await Prefill.items()
        await Prefill.users(1)
        await Prefill.carts()

        # 1 3 2 3 3 | GR1,CF1,SR1,CF1,CF1 -> 30.57€
        await self.item_service.add_to_cart(1, 1)
        await self.item_service.add_to_cart(3, 1)
        await self.item_service.add_to_cart(2, 1)
        await self.item_service.add_to_cart(3, 1)
        await self.item_service.add_to_cart(3, 1)

        await self.rule_engine.apply(1)

        cart_query = await self.cart_service.read_cart({'id': 1})
        actual_cart = cart_query.first()

        self.assertEqual(30.57, actual_cart.total_price)

    async def test_apply_when_cart_not_found_raises_error(self):
        """
        Checks that trying to apply rules to a non existent cart raises exception
        Notes:
            - Arrange: N/A
            - Act: Invoke apply on an arbitrary id on a database with no carts
            - Assert: RuntimeError is raised
        Returns: None

        """
        with self.assertRaises(RuntimeError):
            await self.rule_engine.apply(1)

    def test__sorted_group_by(self):
        """
        Checks that sorted_group_by always groups the same given the same list shuffled
        Notes:
            - Arrange: Build an arbitrary list of objects, shuffle it multiple times
            - Act: Invoke sorted_group_by with the list and an arbitrary expression (must be the same expression though)
            - Assert: Groups are always the same
        Returns: None

        """
        test_list = [{'a': True}, {'a': True}, {'a': True}, {'a': False}, {'a': False}]

        for _ in range(0, 9):
            random.shuffle(test_list)
            groups = self.rule_engine._sorted_group_by(test_list, lambda a: a['a'] is True)
            actual = {}
            for key, group in groups:
                actual.update({key: list(group)})

            self.assertEqual(2, len(actual[False]))
            self.assertEqual(3, len(actual[True]))

    def test__firing_evaluator_when_condition_unmet_it_returns_false(self):
        """
        Notes:
            - Arrange: Build a list of items (< Rule quantity) and create Rule according to TEST_RULE definition
            - Act: Invoke firing_evaluator with the given list and Rule
            - Assert: firing_evaluator returns False
        Returns: None

        """
        items = [Item(name=f'name', code='M22', price=float('1.0')) for _ in range(0,9)]
        rule = Rule(**TEST_RULE)

        self.assertFalse(self.rule_engine._rule_firing_evaluator(items, rule))

    def test__firing_evaluator_when_condition_met_it_returns_true(self):
        """
        Checks that firing_evaluator returns true when condition is met
        Notes:
            - Arrange: Build a list of items (> Rule quantity) and create Rule according to TEST_RULE definition
            - Act: Invoke firing_evaluator with the given list and Rule
            - Assert: firing_evaluator returns True
        Returns: None

        """
        items = [Item(name='name', code='M22', price=float('1.0')) for _ in range(0, 11)]
        rule = Rule(**TEST_RULE)

        self.assertTrue(self.rule_engine._rule_firing_evaluator(items, rule))

    def test__rule_effect_resolver_one_free(self):
        """
        Checks that effect resolver correctly applies effects of type one_free
        Notes:
            - Arrange: Build a list of Items with price 1.0 and create Rule according to TEST_RULE definition
            - Act: Invoke effect_resolver with the given list and Rule
            - Assert: One of the items price is not considered
        Returns: None

        """
        rule_copy = dict(TEST_RULE)
        rule_copy['effect_type'] = 'one_free'
        rule = Rule(**rule_copy)

        items = [Item(name='name', code='M22', price=float('1.0')) for _ in range(0, 2)]
        self.assertEqual(1.0, sum(self.rule_engine._rule_effect_resolver(items, rule)))

        items = [Item(name='name', code='M22', price=float('1.0')) for _ in range(0, 3)]
        self.assertEqual(2.0, sum(self.rule_engine._rule_effect_resolver(items, rule)))

    def test__rule_effect_resolver_update_price(self):
        """
        Checks that effect resolver correctly applies effects of type update_price
        Notes:
            - Arrange: Build a list of Items with price 1.0 and create Rule according to TEST_RULE definition
            - Act: Invoke effect_resolver with the given list and Rule
            - Assert: Total price is 5.0
        Returns: None

        """
        items = [Item(name='name', code='M22', price=float('1.0')) for _ in range(0, 10)]
        rule = Rule(**TEST_RULE)

        self.assertEqual(5.0, sum(self.rule_engine._rule_effect_resolver(items, rule)))

    def test__rule_effect_resolver_when_nonexistent_effect_type_raises_error(self):
        """
        Checks that non existent effect types given a Rule raises RunTime error
        Notes:
            - Arrange: Update a Rule with a non defined effect type
            - Act: Invoke rule effect with the mentioned rule
            - Assert: RunTime exception is raised
        Returns: None

        """
        rule_copy = dict(TEST_RULE)
        rule_copy['effect_type'] = 'unknown'
        rule = Rule(**rule_copy)
        items = [Item(name='name', code='M22', price=float('1.0')) for _ in range(0, 2)]

        with self.assertRaises(RuntimeError):
            _ = self.rule_engine._rule_effect_resolver(items, rule)
