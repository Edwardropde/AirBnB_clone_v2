#!/usr/bin/python3
"""Defines Place Class"""
import models
from os import getenv
from models.base_model import BaseModel
from models.review import Review
from models.base_model import Base
from models.amenity import Amenity
from sqlalchemy import Column
from sqlalchemy.orm import relationship
from sqlalchemy import Integer
from sqlalchemy import ForeignKey
from sqlalchemy import String
from sqlalchemy import Float
from sqlalchemy import Table


association_table = Table("place_amenity", Base.metadata,
                        Column("place_id", String(60),
                            ForeignKey("places.id"),
                            primary_key=True, nullable=False),
                        Column("amenity_id", String(60),
                            ForeignKey("amenities.id"),
                            primary_key=True, nullable=False))


class Place(BaseModel, Base):
    """Represents place in MySQL database

    Inherits from SQLAlchemy Base and links to the MySQL table places.

    Attributes:
        __tablename__ (str): name of MySQL table to store places
        amenity_ids (list): id list of all linked amenities.
        amenities (sqlalchemy relationship): place amenities relationship.
        user_id (sqlalchemy String): Place's user id.
        reviews (sqlalchemy relationship): place-review relationships
        name (sqlalchemy String): name
        longitude (sqlalchemy Float): place's longitude
        description (sqlalchemy String): description
        latitude (sqlalchemy Float): place's latitude
        number_rooms (sqlalchemy Integer): number of rooms.
        price_by_night (sqlalchemy Integer): price during the night
        max_guest (sqlalchemy Integer): max number of guests.
        city_id (sqlalchemy String): place city id.
        number_bathrooms (sqlalchemy Integer): number of bathrooms.
    """
    __tablename__ = "places"
    amenity_ids = []
    amenities = relationship("Amenity", secondary="place_amenity",
                    viewonly=False)
    user_id = Column(String(60), ForeignKey("users.id"), nullable=False)
    reviews = relationship("Review", backref="place", cascade="delete")
    name = Column(String(128), nullable=False)
    longitude = Column(Float)
    description = Column(String(1024))
    latitude = Column(Float)
    number_rooms = Column(Integer, default=0)
    price_by_night = Column(Integer, default=0)
    max_guest = Column(Integer, default=0)
    city_id = Column(String(60), ForeignKey("cities.id"), nullable=False)
    number_bathrooms = Column(Integer, default=0)

    if getenv("HBNB_TYPE_STORAGE", None) is not "db":
        @property
        def reviews(self):
            """Show list of linked reviews"""
            reviewlist = []
            for review in list(models.storage.all(Review).values()):
                if review.place_id == self.id:
                    reviewlist.append(review)
            return reviewlist

        @property
        def amenities(self):
            """Get and set linked amenities"""
            amenitylist = []
            for amenity in list(models.storage.all(Amenity).values()):
                if amenity.id in self.amenity_ids:
                    amenitylist.append(amenity)
            return amenitylist

        @amenities.setter
        def amenities(self, value):
            if isinstance(value, Amenity):
                self.amenity_ids.append(value.id)
