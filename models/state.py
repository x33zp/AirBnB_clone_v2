#!/usr/bin/python3
"""This module creates a User class"""

import os
import models
from models.city import City
from models.base_model import BaseModel, Base
from sqlalchemy.orm import relationship
from sqlalchemy import Column, String


class State(BaseModel, Base):
    """Class for managing state objects"""
    __tablename__ = 'states'

    name = Column(String(128), nullable=False)
    cities = relationship("City", backref="state", cascade="delete")

    if os.getenv('HBNB_TYPE_STORAGE') != 'db':
        @property
        def cities(self):
            """_summary_
            """
            city_list = [city for city in list(models.storage.all(City)
                         .values()) if city.state_id == self.id]
            return city_list