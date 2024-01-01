#!/usr/bin/python3
"""This module defines a class User"""
from models.base_model import BaseModel
from models.base_model import Base
from models import hbnb_type_storage
from models.place import Place
from models.review import Review
from sqlalchemy import Column
from sqlalchemy.orm import relationship
from sqlalchemy import String


class User(BaseModel):
    """
    Represents user in MySQL database
    Inherits from SQLAlchemy Base and connects to MySQL table users

    Attributes:
        __tablename__ (str): Name of MySQL table storing users
        email: (sqlalchemy String): user email
        password (sqlalchemy String): user password
        first_name (sqlalchemy String): user first name
        last_name (sqlalchemy String): user last name
        places (sqlalchemy relationship): user-place relationship
        reviews (sqlalchemy relationship): user-review relationship
    """
    __tablename__ = "users"
    if hbnb_type_storage == 'db':
        email = Column(String(128), nullable=False)
        password = Column(String(128), nullable=False)
        first_name = Column(String(128))
        last_name = Column(String(128))
        places = relationship("Place", backref="user", cascade="delete")
        reviews = relationship("Review", backref="user", cascade="delete")
    else:
        email = ''
        password = ''
        first_name = ''
        last_name = ''
