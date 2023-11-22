#!/usr/bin/python3
"""Defines state class"""
import models
from os import getenv
from models.base_model import BaseModel
from models.base_model import Base
from models.city import City
from sqlalchemy import String
from sqlalchemy import Column
from sqlalchemy.orm import relationship


class State(BaseModel, Base):
    """
    Represents state for MySQL database

    Inherits from SQLAlchemy Base. Connects to MySQL table states

    Attributes:
        __tablename__ (str): The name of the MySQL table to store States.
        cities (sqlalchemy relationship): state-city relationship
        name (sqlalchemy String): state name
    """
    __tablename__ = "states"
    name = Column(String(128), nullable=False)
    cities = relationship(
            'City',
            cascade='all, delete, delete-orphan',
            backref='state'
    ) if getenv('HBNB_TYPE_STORAGE') == 'db' else None
    if getenv('HBNB_TYPE_STORAGE') != 'db':
        @property
        def cities(self):
            """Returns the cities in this State"""
            from models import storage
            cities_in_state = []
            for value in storage.all(City).values():
                if value.state_id == self.id:
                    cities_in_state.append(value)
            return cities_in_state
