#!/usr/bin/python3
"""Defines DBStorage engine"""
from os import getenv
from models.base_model import BaseModel
from models.base_model import Base
from models.amenity import Amenity
from models.state import State
from models.city import City
from models.review import Review
from models.place import Place
from models.user import User
from sqlalchemy.orm import scoped_session
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm import relationship


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
        self.__engine = create_engine("mysql+mysqldb://{}:{}@{}/{}".
                                      format(getenv("HBNB_MYSQL_USER"),
                                             getenv("HBNB_MYSQL_PWD"),
                                             getenv("HBNB_MYSQL_HOST"),
                                             getenv("HBNB_MYSQL_DB")),
                                      pool_pre_ping=True)
        if getenv("HBNB_ENV") == "test":
            Base.metadata.drop_all(self.__engine)

    def all(self, cls=None):
        """
        Query on current database session for objects of specfic class
        If all types of objects are queried, CLS is none
        
        Return:
            Dict of queried classes in '<class name>.<obj id> = obj' format
        """
        try:
            if cls is None:
                all_objs = []
                for model_class in [State, City, User, Place, Review, Amenity]:
                    objs = self.__session.query(model_class).all()
                    all_objs.extend(objs)
            else:
                if type(cls) == str:
                    cls = eval(cls)
                all_objs = self.__session.query(cls).all()
            result_dict = {"{}.{}".format(type(o).__name__, o.id): o for o in all_objs}
            return result_dict
        except Exception as e:
            print(f"Error in all method: {e}")
            return {}

    def new(self, obj):
        """Add object to current database session"""
        self.__session.add(obj)

    def save(self):
        """Commit the changes to current database session"""
        self.__session.commit()

    def delete(self, obj=None):
        """Delete objects from current database session"""
        if obj is not None:
            self.__session.delete(obj)

    def reload(self):
        """Create tables in database and initialize in new session"""
        Base.metadata.create_all(self.__engine)
        session_factory = sessionmaker(bind=self.__engine,
                                       expire_on_commit=False)
        Session = scoped_session(session_factory)
        self.__session = Session()
        for model_class in [State, City, User, Place, Review, Amenity]:
            query = self.__session.query(model_class).all()
            for obj in query:
                key = "{}.{}".format(type(obj).__name__, obj.id)
                self.__objects[key] = obj
        self.__session.close()

    def close(self):
        """Close working SQLAlchemy session"""
        self.__session.close()
