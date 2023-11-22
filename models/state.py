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

    if getenv("HBNB_TYPE_STORAGE") == "db":
        cities = relationship("City", backref="state", cascade="all, delete-orphan")
    else:
        @property
        def cities(self):
            """Get a list of all related City objects."""
            city_list = []
            for city in list(models.storage.all(City).values()):
                if city.state_id == self.id:
                    city_list.append(city)
            return city_list
