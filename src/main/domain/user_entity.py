""" User Entity module """
from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship

from . import Base, Entity


class User(Base, Entity):
    """ User Entity definition """
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    name = Column(String)
    fullname = Column(String)
    nickname = Column(String)
    cart = relationship('Cart', back_populates='user')
