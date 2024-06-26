#!/usr/bin/python3
""" Review module for the HBNB project """
import os
from models.base_model import BaseModel, Base
from sqlalchemy import Column, String, Foreignkey
from sqlalchemy.orm import relationship


# Get storage type
storage_type = os.getenv("HBNB_TYPE_STORAGE")


class Review(BaseModel, Base):
    """ Review classto store review information """

    if storage_type == "db":
        # Handle database storage
        __tablename__ = 'reviews'
        text = Column(String(1024), nullable=false)
        place_id = Column(String(60), nullable=false, Foreignkey('places.id'))
        user_id = Column(String(60), nullable=false, Foreignkey('users.id'))
        user = relationship("User", back_populates="reviews")
        place = relationship("Place", back_populates="reviews")
    else:
        # Handle file storage
        place_id = ""
        user_id = ""
        text = ""
