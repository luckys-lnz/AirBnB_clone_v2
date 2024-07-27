#!/usr/bin/python3
"""
Module defines Database engine `DBStorage`
"""
import os
from models.base_model import Base
from models.user import User
from models.review import Review
from models.place import Place
from models.city import City
from models.state import State
from models.amenity import Amenity
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session


# get the environ variabes
user = os.getenv('HBNB_MYSQL_USER')
passwd = os.getenv('HBNB_MYSQL_PWD')
host = os.getenv('HBNB_MYSQL_HOST')
db = os.getenv('HBNB_MYSQL_DB')
hbnb_env = os.getenv('HBNB_ENV')


class DBStorage:
    """ Defines database engine """

    __engine = None
    __session = None

    def __init__(self):
        """ Initialize database instance """
        self.__engine = create_engine(
            f"mysql+mysqldb://{user}:{passwd}@{host}/{db}", pool_pre_ping=True)

        if hbnb_env == "test":
            # Drop all tables if test environment
            Base.metadata.drop_all(self.__engine)

    def all(self, cls=None):
        """
        Query all objects if cls is None or objects of specified class
        """
        objs_dict = {}
        if cls:
            # Handle class
            for obj in self.__session.query(cls).all():
                key = f"{type(obj).__name__}.{obj.id}"
                objs_dict[key] = obj
        else:
            # Handle all classes
            cls_list = [State, City, User, Review, Place, Amenity]
            for cls in cls_list:
                for obj in self.__session.query(cls).all():
                    key = f"{type(obj).__name__}.{obj.id}"
                    objs_dict[key] = obj
        return objs_dict

    def new(self, obj):
        """ Add object to the current database session """
        self.__session.add(obj)

    def save(self):
        """ Commit all changes to the current database session """
        self.__session.commit()

    def delete(self, obj=None):
        """ Delete from the current database session """
        if obj:
            self.__session.delete(obj)

    def reload(self):
        """ Creates all tables and the current database session """
        Base.metadata.create_all(self.__engine)
        session_factory = sessionmaker(
            bind=self.__engine, expire_on_commit=False)
        Session = scoped_session(session_factory)
        self.__session = Session

    def close(self):
        """ Removes the current session """
        self.__session.remove()
