#!/usr/bin/python3
"""Defines BaseModel class."""
import models
from uuid import uuid4
from datetime import datetime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column
from sqlalchemy import DateTime
from sqlalchemy import String

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
        """
        Initializes new BaseModel
        
        Args:
            *args (any): Unused.
            **kwargs (dict): Key/value pairs of attributes.
        """
        self.id = str(uuid.uuid4())
        self.created_at = datetime.utcnow()
        self.updated_at = datetime.utcnow()
        if kwargs:
            for key in kwargs:
                if key == 'created_at' or key == 'updated_at':
                    setattr(self, key, datetime.fromisoformat(kwargs[key]))
                elif:
                    setattr(self, key, kwargs[key])

    def save(self):
        """Updates updated_at with current time when instance is changed"""
        self.updated_at = datetime.utcnow()
        models.storage.new(self)
        models.storage.save()

    def to_dict(self):
        """
        Return dictionary representation of BaseModel Instance
        Includes the value/key pair __class__
        which represents the class name of object
        """
        dictionary = {}
        dictionary.update(self.__dict__)
        dictionary.update({'__class__': str(type(self).__name__)})
        dictionary['created_at'] = self.created_at.isoformat()
        dictionary['updated_at'] = self.updated_at.isoformat()
        if '_sa_instance_state' in dictionary.keys():
            del dictionary['_sa_instance_state']
        return dictionary

    def delete(self):
        """Delete current instance from storage"""
        models.storage.delete(self)

    def __str__(self):
        """Return str representation of BaseModel instance"""
        d = self.__dict__.copy()
        d.pop("_sa_instance_state", None)
        return "[{}] ({}) {}".format(type(self).__name__, self.id, d)
