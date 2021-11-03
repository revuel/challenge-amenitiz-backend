""" Use Cases: Apply offer rules to a shopping cart to get the final price, CRUD operations for Offers  """
from itertools import groupby
from ..domain.cart_entity import Cart
from ..domain.rule_entity import Rule
from ..infrastructure.database.setup import build_session
from ..infrastructure.database.transaction import Transaction


class RuleService(Transaction):
    """ Offer Rules Service (CRUD operations for Rule Entity) """

    def create_offer_rule(
            self,
            item_code,
            name, description,
            firing_condition_operator,
            firing_condition_quantity,
            effect_type,
            effect_percentage
    ):
        """ Creates a new OfferRule and inserts it to the database """
        with Transaction() as t:
            t.session.add(Rule(
                item_code=item_code,
                name=name,
                description=description,
                firing_condition_operator=firing_condition_operator,
                firing_condition_quantity=firing_condition_quantity,
                effect_type=effect_type,
                effect_percentage=effect_percentage
            ))

    def read_offer_rule(self, filter_params: dict = None):
        """
        Finds a rule at the database according to the provided filters
        Args:
            filter_params: filtering arguments

        Returns: None

        """
        with Transaction() as t:
            return t.session.query(Rule).filter_by(**filter_params)

    async def read_offer_rules(self):
        """ Retrieves all rules from the database """
        with Transaction() as t:
            return t.session.query(Rule)

    def update_offer_rule(self, id: int):
        """
        Updates an existing rule by id
        Args:
            id: Rule's ID

        Returns: None

        """
        raise NotImplementedError

    def delete_rule(self, id):
        """
        Deletes an existing rule by id
        Args:
            id: Rule's ID

        Returns: None

        """
        raise NotImplementedError


class RuleEngine(Transaction):
    """ Rules Engine. Applies rules on carts to compute the final price of the cart """
    def __init__(self, session=None):
        """
        Initializer
        Args:
            session: SQL Alchemy Session instance
        Notes:
             Injectable session to aid Inversion of Control (IoC)
        """
        super().__init__()
        self.session = session if session is not None else build_session()

    async def apply(self, cart_id) -> None:
        """
        Applies existing rules to a specific cart by id. It finally updates the cart total price.
        Args:
            cart_id: Cart's ID

        Returns: None

        """

        with Transaction() as t:
            rules = t.session.query(Rule).all()
            cart = t.session.query(Cart).filter_by(**{'id': cart_id}).first()

            if cart is None:
                raise RuntimeError(f'No Cart with id {cart_id} was found')

            items_with_offers = list()
            applied_offers = list()
            computed_offers_prices = 0
            cart_items = [cart_item.item for cart_item in cart.items]

            for rule in rules:
                groups = self._sorted_group_by(cart_items, lambda i, r=rule: i.code == r.item_code)
                for key, group in groups:
                    if key is True:
                        list_group = list(group)
                        if self._rule_firing_evaluator(list_group, rule) is True:
                            items_with_offers += list_group
                            new_prices = self._rule_effect_resolver(list_group, rule)
                            computed_offers_prices += sum(new_prices)
                            applied_offers.append(rule.name)

            items_with_no_offers = [item for item in cart_items if item not in items_with_offers]
            computed_offers_prices += sum([item.price for item in items_with_no_offers])

            cart.total_price = round(computed_offers_prices, 2)

    def _sorted_group_by(self, iterable, expression):
        """
        This method exist because of this reason: https://docs.python.org/3/library/itertools.html#itertools.groupby
        Assure grouping works irrespectively of the given iterable, previously sorting the iterable with the same
        expression used by the group by
        Args:
            iterable: Iterable
            expression: Expression

        Returns: Iterator

        """
        return groupby(sorted(iterable, key=expression), expression)

    def _rule_firing_evaluator(self, items, rule) -> bool:
        """
        Wether a rule must be fired or not, this method computes the rule precondition returning True if the rule must
        be applied or False otherwise
        Args:
            items: List of Item Entities
            rule: Rule Entity

        Returns: bool

        """
        return eval(f'{len(items)} {rule.firing_condition_operator} {rule.firing_condition_quantity}')

    def _rule_effect_resolver(self, items, rule):
        """
        Applies the rule to the given set of items and computes what price should add this items to the Cart
        Args:
            items: List of Item Entities
            rule: Rule Entity

        Returns: List of int

        """
        new_prices = list()
        if rule.effect_type == 'update_prices':
            new_prices = [item.price - (item.price * rule.effect_percentage) for item in items]
        elif rule.effect_type == 'one_free':
            new_prices = [item.price for item in items]
            new_prices.pop()
        else:
            raise RuntimeError(f'Unknown effect type: {rule.effect_type}')

        return new_prices
