""" Item Entity module """
from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship

from . import Base, Entity


class Item(Base, Entity):
    """ User Entity definition """
    __tablename__ = 'items'

    id = Column(Integer, primary_key=True)
    code = Column(String)
    name = Column(String)
    price = Column(Integer)
    carts = relationship('CartItem', back_populates='item')
