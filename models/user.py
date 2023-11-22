#!/usr/bin/python3
"""Defines user class"""
import os
from models.base_model import BaseModel
from models.base_model import Base
from sqlalchemy.orm import relationship
from sqlalchemy import Column
from sqlalchemy import String


class User(BaseModel, Base):
    """Represents user by various attributes"""
    __tablename__ = 'users'
    email = Column(
            String(128), nullable=False
    ) if os.getenv('HBNB_TYPE_STORAGE') == 'db' else ''
    password = Column(
            String(128), nullable=False
    ) if os.getenv('HBNB_TYPE_STORAGE') == 'db' else ''
    first_name = Column(
            String(128), nullable=True
    ) if os.getenv('HBNB_TYPE_STORAGE') == 'db' else ''
    last_name = Column(
            String(128), nullable=True
    ) if os.getenv('HBNB_TYPE_STORAGE') == 'db' else ''
    places = relationship(
            'Place',
            cascade="all, delete, delete-orphan",
            backref='user'
    ) if os.getenv('HBNB_TYPE_STORAGE') == 'db' else None
    reviews = relationship(
            'Review',
            cascade="all, delete, delete-orphan",
            backref='user'
    ) if os.getenv('HBNB_TYPE_STORAGE') == 'db' else None
