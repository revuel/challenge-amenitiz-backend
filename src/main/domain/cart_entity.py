""" Cart Entity module """
from sqlalchemy import Column, Integer, Float, ForeignKey
from sqlalchemy.orm import relationship, backref
from . import Base, Entity


class Cart(Base, Entity):
    """ Shopping Cart Entity definition """
    __tablename__ = 'carts'

    id = Column(Integer, primary_key=True)
    total_price = Column(Float, default=0.0)
    user_id = Column(Integer, ForeignKey('users.id'))
    user = relationship('User', back_populates='cart')
    items = relationship('CartItem', back_populates='cart')
