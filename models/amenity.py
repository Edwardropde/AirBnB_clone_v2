#!/usr/bin/python3
"""Defines amenity class"""
from sqlalchemy import String
from sqlalchemy import Column
from sqlalchemy.orm import relationship
from models.base_model import BaseModel
from models.base_model import Base


class Amenity(BaseModel, Base):
    """
    Reps amenity for MySQL database.

    Inherits from SQLAlchemy Base and connects to MySQL table amenities

    Attributes:
        name (sqlalchemy String): amenity name
        __tablename__ (str): The name of the MySQL table to store Amenities.
        place_amenities (sqlalchemy relationship): Place-Amenity relationship.
    """
    __tablename__ = "amenities"
    name = Column(String(128), nullable=False)
    place_amenities = relationship("Place", secondary="place_amenity",
            viewonly=False)
