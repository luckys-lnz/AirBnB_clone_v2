#!/usr/bin/python3
import io
import sys
import unittest
from console import HBNBCommand
from models import storage
"""
Module defines a test for `HBNBCommand` a command line interpreter.
"""


class TestConsole(unittest.TestCase):
    """Tests HBNBCommand class"""

    def setUp(self):
        """defines the set up environment for the test"""
        storage.reload()
        self.num_before_obj_creation = len(storage.all())

    def test_do_create(self):
        """test the console create command"""
        # save original
        original_stdout = sys.stdout
        sys.stdout = io.StringIO()
        try:
            console = HBNBCommand()
            console.onecmd('create State name="California"')
            id = sys.stdout.getvalue().strip()
            obj_key = f"State.{id}"

            storage.reload()
            objs = storage.all()

            num_after_obj_creation = len(objs)
            self.assertEqual(
                num_after_obj_creation, self.num_before_obj_creation + 1)
            self.assertIn(obj_key, objs)
            self.assertEqual(objs[obj_key].name, "California")

            # reset stdout
            sys.stdout = io.StringIO()

            console.onecmd('create State name="California" age=[1, 2]')
            id = sys.stdout.getvalue().strip()
            obj_key = f"State.{id}"

            storage.reload()
            objs = storage.all()

            num_after_second_obj_creation = len(objs)
            self.assertEqual(
                num_after_second_obj_creation, num_after_obj_creation + 1)
            self.assertFalse(hasattr(objs[obj_key], 'age'))

        finally:
            sys.stdout = original_stdout
