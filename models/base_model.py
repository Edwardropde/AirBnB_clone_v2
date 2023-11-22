#!/usr/bin/python3
"""Defines BaseModel class."""
import models
from sqlalchemy import Column
from uuid import uuid4
from sqlalchemy import String
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime
from sqlalchemy import DateTime

Base = declarative_base()


class BaseModel:
    """
    Defines BaseModel Class

    Attributes:
        id (sqlalchemy String): BaseModel id
        created_at (sqlalchemy DateTime): datetime at creation.
        updated_at (sqlalchemy DateTime): datetime of last update
    """

    id = Column(String(60), primary_key=True, nullable=False)
    created_at = Column(DateTime, nullable=False, default=datetime.utcnow())
    updated_at = Column(DateTime, nullable=False, default=datetime.utcnow())

    def __init__(self, *args, **kwargs):
        """Initialize new BaseModel

        Args:
            *args (any): Unused.
            **kwargs (dict): value pairs of attributes.
        """
        self.id = str(uuid4())
        self.created_at = self.updated_at = datetime.utcnow()
        if kwargs:
            for key, value in kwargs.items():
                if key == "created_at" or key == "updated_at":
                    value = datetime.strptime(value, "%Y-%m-%dT%H:%M:%S.%f")
                if key != "__class__":
                    setattr(self, key, value)

    def save(self):
        """Updates u_at (last update datetime) with current datetime"""
        self.updated_at = datetime.utcnow()
        models.storage.new(self)
        models.storage.save()

    def to_dict(self):
        """
        Returns dictionary representation of BaseModel Instance.

        Has value pair __class__ representing representing class name of object
        """
        my_dict = self.__dict__.copy()
        my_dict["__class__"] = str(type(self).__name__)
        my_dict["created_at"] = self.created_at.isoformat()
        my_dict["updated_at"] = self.updated_at.isoformat()
        my_dict.pop("_sa_instance_state", None)
        return my_dict

    def delete(self):
        """Deletes current instance from storage"""
        models.storage.delete(self)

    def __str__(self):
        """Returns str representation of BaseModel Instance"""
        d = self.__dict__.copy()
        return "[{}] ({}) {}".format(type(self).__name__, self.id, d)
