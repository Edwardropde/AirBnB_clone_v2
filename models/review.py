#!/usr/bin/python3
"""Defines review class"""
from models.base_model import BaseModel
from models.base_model import Base
from sqlalchemy import Column
from sqlalchemy.orm import relationship
from sqlalchemy import String
from sqlalchemy import ForeignKey


class Review(BaseModel, Base):
    """
    Represents review of MySQL database

    Inherits from SQLAlchemy Base, connects to MySQL table reviews

    Atributes:
        __tablename__ (str): name of Mysql table to store reviews
        user_id (sqlalchemy String): review's user id
        place_id (sqlalchemy String): review's place ide
    """
    __tablename__ = "reviews"
    user_id = Column(String(60), ForeignKey("users.id"), nullable=False)
    place_id = Column(String(60), ForeignKey("places.id"), nullable=False)
