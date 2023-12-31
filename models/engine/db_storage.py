#!/usr/bin/python3
"""Defines DBStorage engine"""
import os
from models.base_model import Base
from models.amenity import Amenity
from models.city import City
from models.place import Place
from models.state import State
from models.review import Review
from models.user import User
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session
name2class = {
    'Amenity': Amenity,
    'City': City,
    'Place': Place,
    'State': State,
    'Review': Review,
    'User': User
}


class DBStorage:
    """
    Represents database storage engine

    Attributes:
        __engine (sqlalchemy.Engine): working SQLAlchemy engine
        __session (sqlalchemy.Session): working SQLAlchemy seesion
    """

    __engine = None
    __session = None

    def __init__(self):
        """Initialize new DBStorage Instance"""
        user = os.getenv('HBNB_MYSQL_USER')
        host = os.getenv('HBNB_MYSQL_HOST')
        passwd = os.getenv('HBNB_MYSQL_PWD')
        database = os.getenv('HBNB_MYSQL_DB')
        self.__engine = create_engine('mysql+mysqldb://{}:{}@{}/{}'
                                      .format(user, passwd, host, database))
        if os.getenv('HBNB_ENV') == 'test':
            Base.metadata.drop_all(self.__engine)

    def all(self, cls=None):
        """
        Query on current database session for objects of specfic class
        If all types of objects are queried, CLS is none
        
        Return:
            Dict of queried classes in '<class name>.<obj id> = obj' format
        """
        if not self.__session:
            self.reload()
        objects = {}
        if type(cls) == str:
            cls = name2class.get(cls, None)
        if cls:
            for obj in self.__session.query(cls):
                objects[obj.__class__.__name__ + '.' + obj.id] = obj
        else:
            for cls in name2class.values():
                for obj in self.__session.query(cls):
                    objects[obj.__class__.__name__ + '.' + obj.id] = obj
        return objects

    def new(self, obj):
        """Add object to current database session"""
        self.__session.add(obj)

    def save(self):
        """Commit the changes to current database session"""
        self.__session.commit()

    def delete(self, obj=None):
        """Delete objects from current database session"""
        if not self.__session:
            self.reload()
        if obj:
            self.__session.delete(obj)

    def reload(self):
        """Create tables in database and initialize in new session"""
        Base.metadata.create_all(self.__engine)
        session_factory = sessionmaker(bind=self.__engine,
                                       expire_on_commit=False)
        self.__session = scoped_session(session_factory)

    def close(self):
        """Close working SQLAlchemy session"""
        self.__session.close()

    def get(self, cls, id):
        """Retrieve object"""
        if cls is not None and type(cls) is str and id is not None and\
           type(id) is str and cls in name2class:
               cls = name2class[cls]
               result = self.__session.query(cls).filter(cls.id == id).first()
               return result
        else:
            return None

    def count(self, cls=None):
        """Count number of objects in storage"""
        total = 0
        if type(cls) == str and cls in name2class:
            cls = name2class[cls]
            total = self.__session.query(cls).count()
        elif cls is None:
            for cls in name2class.values():
                total += self.__session.query(cls).count()
        return total
