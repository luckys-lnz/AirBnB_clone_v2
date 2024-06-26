#!/usr/bin/python3
""" Place Module for HBNB project """

from models.base_model import BaseModel, Base
from sqlalchemy import Integer, Column, String, Float, ForeignKey
from sqlalchemy.orm import relationship


class Place(BaseModel, Base):
    """ A place to stay """
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

    user = relationship('User', back_populates='places')
    city = relationship('City', back_populates='places')
    reviews = relationship('Review', back_populates='place',
                           cascade='all, delete-orphan')

    if models.storage_t == 'db':
        reviews = relationship('Review', back_populates='place',
                               cascade='all', delete-orphan)
    else:
        @property
        def reviews(self):
            """ file storage getter for relationship btwn places and review """
            return [review for review in models.storage.all(Review).values()
                    if review.place_id == self.id]
