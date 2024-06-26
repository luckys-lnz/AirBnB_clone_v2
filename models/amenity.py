#!/usr/bin/python3
""" State Module for HBNB project """
import os
from sqlalchemy import Column, String, ForeignKey
from sqlalchemy.orm import relationship
from models.base_model import BaseModel, Base
from models.place import place_amenity

# Get the storage type
storage_type = os.getenv("HBNB_TYPE_STORAGE")


class Amenity(BaseModel, Base):
    """ Defines Amenity class """

    if storage_type == "db":
        __tablename__ = 'amenities'
        # Handle database storage
        name = Column(String(128), nullable=False)

        # Many-to-Many relationship
        place_amenities = relationship('Place',
                                       secondary='place_amenity',
                                       back_populates='amenities',
                                       viewonly=False)
    else:
        # Handle file storage
        name = ""
