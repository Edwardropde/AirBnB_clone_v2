#!/usr/bin/python3
"""Defines user class"""
from models.base_model import BaseModel
from models.base_model import Base
from sqlalchemy.orm import relationship
from sqlalchemy import Column
from sqlalchemy import String


class User(BaseModel, Base):
    """
    Represents user for MySQL database

    Inherits from SQLAlchemy Base. Conects to MySQL table users

    Attributes:
        __tablename__ (str): name of Mysql table to store users
        places (sqlalchemy relationship): User-Place relationship.
        email: (sqlalchemy String): user's email address.
        reviews (sqlalchemy relationship): User-Review relationship.
        first_name (sqlalchemy String): user first name
        last_name (sqlalchemy String): user last name
        password (sqlalchemy String): user password
    """
    __tablename__ = "users"
    email = Column(String(128), nullable=False)
    password = Column(String(128), nullable=False)
    first_name = Column(String(128), nullable=True)
    last_name = Column(String(128), nullable=True)
