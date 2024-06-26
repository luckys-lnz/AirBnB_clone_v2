#!/usr/bin/python3
""" Place Module for HBNB project """
import os
from models.base_model import BaseModel, Base
from sqlalchemy import Integer, Column, String, Float, ForeignKey
from sqlalchemy.orm import relationship


# Get storage type
storage_type = os.getenv("HBNB_TYPE_STORAGE")


class Place(BaseModel, Base):
    """ A place to stay """
    if storage_type == "db":
        # Handle database storage
        __tablename__ = 'places'
        city_id = Column(String(60), nullable=False, Foreignkey('cities.id'))
        user_id = Column(String(60), nullable=False, Foreignkey('users.id'))
        name = Column(String(128), nullable=False)
        description = Column(String(1024), nullable=True)
        number_rooms = Column(Integer, default=0, nullable=False)
        number_bathrooms = Column(Integer, default=0, nullable=False)
        max_guest = Column(Integer, default=0, nullable=False)
        price_by_night = Column(Integer, default=0, nullable=False)
        latitude = Column(Float, nullable=True)
        longitude = Column(Float, nullable=True)
        amenity_ids = []
        # relationships
        user = relationship('User', back_populates='places')
        city = relationship('City', back_populates='places')
        reviews = relationship('Review', back_populates='place',
                           cascade='all, delete-orphan')
    else:
        # Handle file storage
        city_id = ""
        user_id = ""
        name = ""
        description = ""
        number_rooms = 0
        number_bathrooms = 0
        max_guest = 0
        price_by_night = 0
        latitude = 0.0
        longitude = 0.0
        amenity_ids = []

        # public getter method -- get reviews
        @property
        def reviews(self):
            """ file storage getter for relationship btwn places and review """
            from models import storage
            return [review for review in storage.all(Review).values()
                    if review.place_id == self.id]
