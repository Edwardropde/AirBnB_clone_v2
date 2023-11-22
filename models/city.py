#!/usr/bin/python3
"""Defines City class"""
import os
from sqlalchemy import ForeignKey
from models.base_model import Base
from sqlalchemy import String
from models.base_model import BaseModel
from sqlalchemy.orm import relationship
from sqlalchemy import Column


class City(BaseModel, Base):
    """
    Represents city for MySQL database

    Inherits from SQLAlchemy Base and links to the MySQL table cities.

    Attributes:
        name (sqlalchemy String): city name
        __tablename__ (str): name of MySQL table to store cities
        state_id (sqlalchemy String): state id of city
    """
    __tablename__ = "cities"
    name = Column(String(128), nullable=False)
    state_id = Column(String(60), ForeignKey('states.id'), nullable=False)
    places = relationship(
            'Place',
            cascade='all, delete, delete-orphan',
            backref='cities'
    ) if os.getenv('HBNB_TYPE_STORAGE') == 'db' else None
