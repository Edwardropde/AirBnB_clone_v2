#!/usr/bin/python3
"""Defines DBStorage engine"""
import os
from os import getenv
from models.base_model import BaseModel
from models.base_model import Base
from models.user import User
from models.amenity import Amenity
from models.city import City
from models.state import State
from models.place import Place
from models.review import Review
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm import scoped_session
from sqlalchemy.orm import relationship


class DBStorage:
    """
    Represents database storage engine

    Attributes:
        __engine (sqlalchemy.Engine): working SQLAlchemy engine.
        __session (sqlalchemy.Session): working SQLAlchemy session.
    """

    __engine = None
    __session = None

    def __init__(self):
        """Initialize new dbstorage instance"""
        user = os.getenv('HBNB_MYSQL_USER')
        password = os.getenv('HBNB_MYSQL_PWD')
        localhost = os.getenv('HBNB_MYSQL_HOST')
        db_name = os.getenv('HBNB_MYSQL_DB')
        env = os.getenv('HBNB_ENV')
        DATABASE_URL = "mysql+mysqldb://{}:{}@{}:3306/{}".format(
                user, password, localhost, db_name
        )
        self.__engine = create_engine(
                DATABASE_URL,
                pool_pre_ping=True
        )
        if env == 'test':
            Base.metadata.drop_all(self.__engine)

    def all(self, cls=None):
        """
        Query on current database session for objects of a particular class

        Queries all types of objects otherwise None if cls is none

        Return:
            Dictionary queried classes in the <class name>.<obj id> = obj.
        """
        objects = dict()
        all_classes = (User, State, City, Amenity, Place, Review)
        if cls is None:
            for class_type in all_classes:
                query = self.__session.query(class_type)
                for obj in query.all():
                    obj_key = '{}.{}'.format(obj.__class__.__name__, obj.id)
                    objects[obj_key] = obj
        else:
            query = self.__session.query(cls)
            for obj in query.all():
                obj_key = '{}.{}'.format(obj.__class__.__name__, obj.id)
                objects[obj_key] = obj
        return objects

    def new(self, obj):
        """Add object to current database session"""
        if obj is not None:
            try:
                self.__session.add(obj)
                self.__session.flush()
                self.__session.refresh(obj)
            except Exception as ex:
                self.__session.rollback()
                raise ex

    def save(self):
        """commit changes to current database session"""
        self.__session.commit()

    def delete(self, obj=None):
        """Delete object from current database session"""
        if obj is not None:
            self.__session.query(type(obj)).filter(
                    type(obj).id == obj.id).delete(
                    synchronize_session=False
            )

    def reload(self):
        """Creayes all table in database and initialize new session"""
        Base.metadata.create_all(self.__engine)
        session_factory = sessionmaker(
                bind=self.__engine, expire_on_commit=False)
        Session = scoped_session(session_factory)

    def close(self):
        """Close working SQLAlchemy session"""
        self.__session.close()
