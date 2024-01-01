#!/usr/bin/python3
""" Review module for the HBNB project """
from models.base_model import BaseModel
from models.base_model import Base
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy import Column
from sqlalchemy import String


class Review(BaseModel):
    """
    Represents review in MySQL database
    Inherts from SQLAlchemy Base and conects to MySQL table reviews

    Attributes:
        __tablename__ (str): name of MySQL table to store reviews
        text (sqlalchemy String): Review description
        place_id (sqlalchemy String): Review's place id
        user_id (sqlalchemy String) Review user id
    """
    __tablename__ = "reviews"
    text = Column(String(1024), nullable=False)
    place_id = Column(String(60), ForeignKey('places.id'), nullable=False)
    user_id = Column(String(60), ForeignKey('users.id'), nullable=False)
