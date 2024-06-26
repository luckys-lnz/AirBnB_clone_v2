#!/usr/bin/python3
""" State Module for HBNB project """
import os
from models.base_model import Base
from models.base_model import BaseModel
from sqlalchemy import Column, String
from sqlalchemy.orm import relationship


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
                                       viewonly=False)
    else:
        # Handle file storage
        name = ""
