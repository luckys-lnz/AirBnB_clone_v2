#!/usr/bin/python3
""" State Module for HBNB project """
import os
from sqlalchemy import Column, String
from sqlalchemy.orm import relationship
from models.city import City
from models.base_model import BaseModel, Base


# Get storage type
storage_type = os.getenv("HBNB_TYPE_STORAGE")


class State(BaseModel, Base):
    """ State class """

    if storage_type == "db":
        # Handle DB storage
        __tablename__ = 'states'
        name = Column(String(128), nullable=False)
        cities = relationship(
            'City', backref='state', cascade='all, delete, delete-orphan')
    else:
        # Handle File storage
        name = ""

        @property
        def cities(self):
            """
            Returns: list of `City` instances of the current `State` object
            """
            from models import storage
            # empty cities list
            state_cities = []

            # get list of cities
            cities = storage.all(City)
            for city_obj in cities.values():
                if city_obj.state_id == self.id:
                    state_cities.append(str(city_obj))

            return state_cities
