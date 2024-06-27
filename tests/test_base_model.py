#!/usr/bin/python3
"""
Module defines a test for the `BaseModel` class
"""
import time
import unittest
from datetime import datetime
from models.base_model import BaseModel


class TestBaseModel(unittest.TestCase):
    """
    Test BaseModel class
    """
    def setUp(self):
        """create object used in the test methods"""
        self.obj = BaseModel()

    def test_class_attributes(self):
        """tests instance attributes"""
        self.assertIsInstance(self.obj.id, str)
        self.assertIsInstance(self.obj.created_at, datetime)
        self.assertIsInstance(self.obj.updated_at, datetime)

    def test_str_method(self):
        """tests __str__ method"""
        obj_str = "[{}] ({}) {}".format(
                  type(self.obj).__name__, self.obj.id, self.obj.__dict__)
        self.assertEqual(str(self.obj), obj_str)

    def test_save_method(self):
        """tests save method"""
        prev_time = self.obj.updated_at

        # delay execution of next line of code
        time.sleep(1)

        # update the object
        self.obj.save()

        curr_time = self.obj.updated_at

        self.assertNotEqual(curr_time, prev_time)

    def test_to_dict_method(self):
        """tests to_dict method"""

        # create a dict
        obj_dict = self.obj.to_dict()
        cls_name = obj_dict.get('__class__')

        self.assertIn('id', obj_dict)
        self.assertIn('created_at', obj_dict)
        self.assertIn('updated_at', obj_dict)
        self.assertIn('__class__', obj_dict)

        self.assertIn(cls_name, 'BaseModel')

        self.assertIsInstance(obj_dict['created_at'], str)
        self.assertIsInstance(obj_dict['updated_at'], str)

    def test_kwargs_passed(self):
        """tests for object created from dictionary"""

        # create the dict
        obj_dict = self.obj.to_dict()

        # create object
        new_obj = BaseModel(**obj_dict)

        self.assertNotIn('__class__', new_obj.__dict__)
        self.assertIsInstance(new_obj.created_at, datetime)
        self.assertIsInstance(new_obj.updated_at, datetime)
