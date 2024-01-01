#!/usr/bin/python3
""" State Module for HBNB project """
import models
from models.base_model import BaseModel, Base
from os import getenv
from models.city import City
from sqlalchemy.orm import relationship
from sqlalchemy import Column
from sqlalchemy import String


class State(BaseModel, Base):
    """
    Represents state for MySQL database
    Inherits from SPLAlchemy Base and connects to MySQL table states
    
    Attributes:
        __tablename__ (str): Name of MySQL table to store states
        name (sqlalchemy String): name of state
        cities (sqlalchemy relationship): state city connection
    """
    __tablename__ = "states"
    if models.hbnb_type_storage == 'db':
        name = Column(String(128), nullable=False)
        cities = relationship("City", cascade="all, delete", backref="states")
    else:
        name = ''

    @property
    def cities(self):
        """Get list of related city objects"""
        _cities = []
        cities = models.storage.all(City)
        for city in cities.values():
            if city.state_id == self.id:
                _cities.append(city)
        return _cities
