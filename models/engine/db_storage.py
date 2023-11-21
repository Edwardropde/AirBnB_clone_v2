#!/usr/bin/python3
"""Defines DBStorage engine"""
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
        Query on current database session for objects of a particular class

        Queries all types of objects otherwise None if cls is none

        Return:
            Dictionary queried classes in the <class name>.<obj id> = obj.
        """
        if cls is None:
            objs = self.__session.query(State).all()
            objs.extend(self.__session.query(User).all())
            objs.extend(self.__session.query(Place).all())
            objs.extend(self.__session.query(City).all())
            objs.extend(self.__session.query(Amenity).all())
            objs.extend(self.__session.query(Review).all())
        else:
            if type(cls) is str:
                cls = eval(cls)
            objs = self.__session.query(cls)
        return {"{}.{}".format(type(o).__name__, o.id): o for o in objs}

    def new(self, obj):
        """Add object to current database session"""
        self.__session.add(obj)

    def save(self):
        """commit changes to current database session"""
        self.__session.commit()

    def delete(self, obj=None):
        """Delete object from current database session"""
        if obj is not None:
            self.__session.delete(obj)

    def reload(self):
        """Creayes all table in database and initialize new session"""
        Base.metadata.create_all(self.__engine)
        session_factory = sessionmaker(bind=self.__engine,
                                        expire_on_commit=False)
        Session = scoped_session(session_factory)
        self.__session = Session()

    def close(self):
        """Close working SQLAlchemy session"""
        self.__session.close()