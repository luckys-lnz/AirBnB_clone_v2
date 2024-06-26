#!/usr/bin/python3
"""
This module defines a base class for all models in our hbnb clone
"""
import os
import uuid
from datetime import datetime
from sqlalchemy import Column, String, DateTime
from sqlalchemy.ext.declarative import declarative_base


# Get storage type
storage_type = os.getenv("HBNB_TYPE_STORAGE")
if storage_type == "db":
    Base = declarative_base()
else:
    Base = object


def generate_uuid():
    return str(uuid.uuid4())


class BaseModel:
    """A base class for all hbnb models"""
    if storage_type == "db":
        id = Column(
            String(60), primary_key=True, nullable=False,
            default=generate_uuid)
        created_at = Column(DateTime, nullable=False, default=datetime.utcnow)
        updated_at = Column(DateTime, nullable=False, default=datetime.utcnow)

    # Handle File storage
    def __init__(self, *args, **kwargs):
        """Instantiates a new model"""
        if kwargs:
            if 'updated_at' in kwargs:
                # recreate obj -- from to_dict()
                kwargs['updated_at'] = datetime.strptime(
                    kwargs['updated_at'], '%Y-%m-%dT%H:%M:%S.%f')
            else:
                # new obj
                self.updated_at = datetime.now()

            if 'created_at' in kwargs:
                # recreate obj -- from to_dict()
                kwargs['created_at'] = datetime.strptime(
                    kwargs['created_at'], '%Y-%m-%dT%H:%M:%S.%f')
            else:
                # new obj
                self.created_at = datetime.now()

            if 'id' not in kwargs:
                # new obj
                self.id = str(uuid.uuid4())

            if '__class__' in kwargs:
                # recreate obj -- from to_dict()
                del kwargs['__class__']

            # set attribute to the instance
            for attr_name, attr_value in kwargs.items():
                setattr(self, attr_name, attr_value)

        else:
            self.id = str(uuid.uuid4())
            self.created_at = datetime.now()
            self.updated_at = datetime.now()

    def __str__(self):
        """Returns a string representation of the instance"""
        cls = (str(type(self)).split('.')[-1]).split('\'')[0]
        return '[{}] ({}) {}'.format(cls, self.id, self.__dict__)

    def save(self):
        """Updates updated_at with current time when instance is changed"""
        from models import storage
        self.updated_at = datetime.now()
        storage.new(self)
        storage.save()

    def to_dict(self):
        """
        Returns: dictionary containing all key/values of __dict__ of the
        instance
        """
        obj_dict = {}
        for key, value in self.__dict__.items():
            if key == "created_at" or key == "updated_at":
                obj_dict[key] = datetime.isoformat(value)
            else:
                obj_dict[key] = value
        obj_dict["__class__"] = type(self).__name__
        if '_sa_instance_state' in obj_dict:
            del obj_dict['_sa_instance_state']

        return obj_dict

    def delete(self):
        """Deletes the current instance from storage"""
        from models import storage
        storage.delete(self)
