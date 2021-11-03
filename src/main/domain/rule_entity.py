""" Rule Entity module """
from sqlalchemy import Column, Integer, String, Float
from . import Base, Entity


class Rule(Base, Entity):
    """ Rule Entity definition """
    __tablename__ = 'rules'

    id = Column(Integer, primary_key=True)
    item_code = Column(String)
    name = Column(String)
    description = Column(String)
    firing_condition_operator = Column(String)
    firing_condition_quantity = Column(Integer)
    effect_type = Column(String)
    effect_percentage = Column(Float)
