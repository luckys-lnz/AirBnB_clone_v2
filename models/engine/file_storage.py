#!/usr/bin/python3
"""This module defines a class to manage file storage for hbnb clone"""
import json


class FileStorage:
    """This class manages storage of hbnb models in JSON format"""
    __file_path = 'file.json'
    __objects = {}

    def all(self, cls=None):
        """
        Returns a list of objects of one type, if class is provided
        or all objects if cls is None.
        """
        # retrieve all objects
        objs_dict = FileStorage.__objects

        if cls is None:
            return objs_dict
        else:
            # create empty object dict
            cls_objects = {}

            for key, obj in objs_dict.items():
                if isinstance(obj, cls):
                    # if cls is found add item to cls_objects
                    cls_objects[key] = obj

            return cls_objects

    def new(self, obj):
        """Adds new object to storage dictionary"""
        self.all().update({obj.to_dict()['__class__'] + '.' + obj.id: obj})

    def save(self):
        """Saves storage dictionary to file"""
        with open(FileStorage.__file_path, 'w') as f:
            temp = {}
            temp.update(FileStorage.__objects)
            for key, val in temp.items():
                temp[key] = val.to_dict()
            json.dump(temp, f)

    def reload(self):
        """Loads storage dictionary from file"""
        from models.base_model import BaseModel
        from models.user import User
        from models.place import Place
        from models.state import State
        from models.city import City
        from models.amenity import Amenity
        from models.review import Review

        classes = {
                    'BaseModel': BaseModel, 'User': User, 'Place': Place,
                    'State': State, 'City': City, 'Amenity': Amenity,
                    'Review': Review
                  }
        try:
            temp = {}
            with open(FileStorage.__file_path, 'r') as f:
                temp = json.load(f)
                for key, val in temp.items():
                    self.all()[key] = classes[val['__class__']](**val)
        except FileNotFoundError:
            pass

    def delete(self, obj=None):
        """Deletes an object from __objects"""
        # handle: obj is None
        if obj is None:
            pass

        # get the object key
        obj_key = "{}.{}".format(type(obj).__name__, obj.id)

        # retrieve objects dict from __objects
        objs_dict = self.all()

        if obj_key in objs_dict:
            del objs_dict[obj_key]
