#!/usr/bin/python3
""" City Module for HBNB project """
from models.base_model import BaseModel
from models.base_model import Base
from models.place import Place
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy import Column
from sqlalchemy import String


class City(BaseModel, Base):
    """
    Represents city in MySQL database
    Inherits from SQLAlchemy Base and connects to the MySQL table cities

    Attributes:
        __tablename__ (str): name of MySQL table storing cities
        name (sqlalchemy String): name of city
        state_id (sqlalchemy String): state id of city
    """
    __tablename__ = "cities"
    name = Column(String(128), nullable=False)
    state_id = Column(String(60), ForeignKey("states.id"), nullable=False)
    places = relationship("Place", backref="cities", cascade="delete")
