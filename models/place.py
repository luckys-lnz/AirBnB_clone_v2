#!/usr/bin/python3
""" Place Module for HBNB project """
import os
from models.base_model import BaseModel, Base
from sqlalchemy import Integer, Column, String, Float, ForeignKey
from sqlalchemy.orm import relationship


# Get storage type
storage_type = os.getenv("HBNB_TYPE_STORAGE")


# Association table -- place_amenity
place_amenity = Table('place_amenity', Base.metadata,
    Column(
        'place_id', String(60), ForeignKey('places.id'), primary_key=True)
    Column(
        'amenity_id', String(60), ForeignKEY('amenities.id'), primary_key=True)
)


class Place(BaseModel, Base):
    """ A place to stay """
    if storage_type == "db":
        # Handle database storage
        __tablename__ = 'places'
        city_id = Column(String(60), ForeignKey('cities.id'), nullable=False)
        user_id = Column(String(60), ForeignKey('users.id'), nullable=False)
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
        reviews = relationship('Review', backref='place',
                               cascade='all, delete-orphan')
        amenities = relationship('Amenity', secondary=place_amenity,
                                 backref='place', viewonly=False)
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
