""" CartItem Entity module """
from sqlalchemy import Column, Integer, ForeignKey
from sqlalchemy.orm import relationship
from . import Base, Entity


class CartItem(Base, Entity):
    """ Shopping Cart - Item Relationship Entity definition """
    __tablename__ = 'items_to_carts'

    id = Column(Integer, primary_key=True)
    items_id = Column(ForeignKey('items.id'))
    carts_id = Column(ForeignKey('carts.id'))
    item = relationship('Item', back_populates='carts')
    cart = relationship('Cart', back_populates='items')
