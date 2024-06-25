#!/usr/bin/python3
"""
Module defines Database engine `DBStorage`
"""
import os
from models.amenity import Amenity
from models.city import City
from models.place import Place
from models.review import Review
from models.state import State
from models.user import User
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session
from sqlalchemy.ext.declarative import declarative_base


# get the environ variabes
user = os.getenv('HBNB_MYSQL_USER')
passwd = os.getenv('HBNB_MYSQL_PWD')
host = os.getenv('HBNB_MYSQL_HOST')
db = os.getenv('HBNB_MYSQL_DB')
hbnb_env = os.getenv('HBNB_ENV')


# defines Base class
Base = declarative_base()


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
        obj_dict = {}
        if cls:
            # Handle cls provided
            for obj in self.__session.query(cls).all():
                key = f"{type(obj).__name__}.{obj.id}"
                objs_dict[key] = obj
        else:
            # Handle cls is None

            for mapped_class in Base._decl_class_registry.values():
                # Validate
                if isinstance(mapped_class, type) and issubclass(mapped_class, Base):
                    for obj in self.__session.query(mapped_class).all():
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
        session_factory = sessionmaker(bind=self.__engine, expire_on_commit=False)
        Session = scoped_session(session_factory)
        self.__session = Session()
