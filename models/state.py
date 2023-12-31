#!/usr/bin/python3
""" State Module for HBNB project """
import models
from models.base_model import BaseModel, Base
from os import getenv
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

    if getenv('HBNB_TYPE_STORAGE') == 'db':
        __tablename__ = "states"
        name = Column(String(128), nullable=False)
        cities = relationship("City", cascade="all, delete",
                              backref="states")
    else:
        name = ""

    def __init__(self, *args, **kwargs):
        """initializes state"""
        super().__init__(*args, **kwargs)

    if getenv("HBNB_TYPE_STORAGE") != "db":
        @property
        def cities(self):
            """Get a list of all related City objects."""
            city_val = models.storage.all("City").values()
            city_list = []
            for city in city_val:
                if city.state_id == self.id:
                    city_list.append(city)
            return city_list

if __name__ == "__main__":
    Base.metadata.create_all(models.storage._DBStorage__engine)
