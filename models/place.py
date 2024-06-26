#!/usr/bin/python3
"""Place module.

This module which inherits from BaseModel defines the Place
class.
"""

import os
import models
from models.base_model import BaseModel, Base
from sqlalchemy import Integer, String, Float
from sqlalchemy import Column, ForeignKey, Table
from sqlalchemy.orm import relationship
from models.review import Review
from models.amenity import Amenity

place_amenity = Table(
    'place_amenity', Base.metadata,
    Column('place_id', String(60), ForeignKey('places.id'),
           primary_key=True, nullable=False),
    Column('amenity_id', String(60), ForeignKey('amenities.id'),
           primary_key=True, nullable=False)
)


class Place(BaseModel, Base):
    """This class represents a Place."""
    __tablename__ = 'places'

    city_id = Column(String(60), ForeignKey('cities.id'), nullable=False)
    user_id = Column(String(128), ForeignKey('users.id'), nullable=False)
    name = Column(String(128), nullable=False)
    description = Column(String(1024), nullable=True)
    number_rooms = Column(Integer, nullable=False, default=0)
    number_bathrooms = Column(Integer, nullable=False, default=0)
    max_guest = Column(Integer, nullable=False, default=0)
    price_by_night = Column(Integer, nullable=False, default=0)
    latitude = Column(Float, nullable=True)
    longitude = Column(Float, nullable=True)
    amenity_ids = []
    reviews = relationship("Review", backref="place", cascade="delete")
    amenities = relationship("Amenity", secondary=place_amenity,
                             viewonly=False, overlaps='place_amenities')

    if os.getenv('HBNB_TYPE_STORAGE') != 'db':
        @property
        def reviews(self):
            """_summary_
            """
            review_list = [review for review in list(models.storage.all(Review)
                           .values()) if review.place_id == self.id]
            return review_list

        @property
        def amenities(self):
            """_summary_
            """
            amenity_list = [amenity for amenity in
                            list(models.storage.all(Amenity)
                                 .values()) if amenity.id in self.amenity_ids]
            return amenity_list

        @amenities.setter
        def amenities(self, value):
            """_summary_
            """
            if isinstance(value, Amenity):
                self.amenity_ids.append(value.id)
