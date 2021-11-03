""" Use Case: populate/prefill the database with random data for testing purposes """
from ..domain.cart_entity import Cart
from ..domain.item_entity import Item
from ..domain.rule_entity import Rule
from ..domain.user_entity import User
from ..infrastructure.database.transaction import Transaction


class Prefill(object):
    """ Database prefilling class. Utility both for unit testing and challenge commodity """

    @staticmethod
    async def users(amount: int = 10) -> None:
        """
        Inserts an amount number of randomized users to the database
        Args:
            amount: Number of random users to insert

        Notes:
            The Transaction context manager is used in order to insert all the desired users in the same transaction

        Returns: None

        """
        with Transaction() as t:
            for i in range(0, amount):
                t.session.add(User(name=f'name_{i}', fullname=f'full_{i}', nickname=f'nick_{i}'))

    @staticmethod
    async def items() -> None:
        """
        Inserts challenge defined items to the database
        Returns: None

        """
        challenge_items = [
            {'code': 'GR1', 'name': 'Green Tea', 'price': 3.11},
            {'code': 'SR1', 'name': 'Strawberries', 'price': 5.00},
            {'code': 'CF1', 'name': 'Coffee', 'price': 11.23},
        ]

        with Transaction() as t:
            for challenge_item in challenge_items:
                t.session.add(Item(**challenge_item))

    @staticmethod
    async def rules() -> None:
        """
        Inserts challenge defined offer rules to the database
        Returns: None

        """
        challenge_rules = [
            {
                'item_code': 'GR1',
                'name': 'buy-one-get-one-free',
                'description': f'The CEO is a big fan of buy-one-get-one-free offers and green tea.'
                               f'He wants us to add a rule to do this',
                'firing_condition_operator': '>=',
                'firing_condition_quantity': 2,
                'effect_type': 'one_free',
                'effect_percentage': None,
            },
            {
                'item_code': 'SR1',
                'name': 'bulk-strawberries',
                'description': f'The COO, though, likes low prices and wants people buying strawberries to get a price'
                               f'discount for bulk purchases. If you buy 3 or more strawberries, the price should drop '
                               f'to 4.50€.',
                'firing_condition_operator': '>=',
                'firing_condition_quantity': 3,
                'effect_type': 'update_prices',
                'effect_percentage': 0.1
            },
            {
                'item_code': 'CF1',
                'name': 'coffee-addiction',
                'description': f'The VP of Engineering is a coffee addict. If you buy 3 or more coffees, the price of '
                               f'all coffees should drop to 2/3 of the original price.',
                'firing_condition_operator': '>=',
                'firing_condition_quantity': 3,
                'effect_type': 'update_prices',
                'effect_percentage': 0.3333333
            }
        ]

        with Transaction() as t:
            for challenge_rule in challenge_rules:
                t.session.add(Rule(**challenge_rule))

    @staticmethod
    async def carts() -> None:
        """
        Adds a cart for each current existing user on the database
        Returns: None

        """
        with Transaction() as t:
            users = t.session.query(User).all()
            for user in users:
                t.session.add(Cart(user=user))

    @staticmethod
    async def all() -> None:
        """
        Aggregator method to prefill the whole database with sample data
        Returns: None

        """
        await Prefill.users()
        await Prefill.items()
        await Prefill.rules()
        await Prefill.carts()
