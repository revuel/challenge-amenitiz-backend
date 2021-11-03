""" Domain Layer. Chosen modelling tool is sqlalchemy, so declarative base definition goes here """
from typing import Dict
from sqlalchemy import inspect
from sqlalchemy.orm import declarative_base

from ..infrastructure.logging.logger import LOGGER


Base = declarative_base()


class Entity(object):
    """ Common Domain Entity utilities """

    def __init__(self, *args, **kwargs):
        """
        Empty init with *args and **kwargs to not collide with SQL Alchemy Base class when inheriting from both classes
        Args:
            *args: arguments
            **kwargs: keyword arguments
        """
        pass

    def __repr__(self) -> str:
        """
        Simple entity representation
        Returns: String representing User Entity

        """
        return f'{self.__class__.__name__}({self.to_dict()})'

    def to_dict(self) -> Dict:
        """
        A more proper dict representation for this class (does not handle relationships)
        Returns: dict representing User Entity

        """
        return {c.key: getattr(self, c.key) for c in inspect(self).mapper.column_attrs}

    @classmethod
    def enroll(cls) -> None:
        """
        Logs an informative message
        Returns: None

        """
        LOGGER.debug(f'Enrolling {cls.__name__}')
