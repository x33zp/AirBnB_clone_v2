#!/usr/bin/python3
"""Amenity module.

This module which inherits from BaseModel defines the
Amenity class.
"""
import os
from models.base_model import BaseModel, Base
from sqlalchemy import Column, String
from sqlalchemy.orm import relationship


class Amenity(BaseModel, Base):
    """This class represents Amenity."""
    __tablename__ = 'amenities'

    name = Column(String(128), nullable=False)
    place_amenities = relationship('Place', secondary='place_amenity',
                                       viewonly=False)
