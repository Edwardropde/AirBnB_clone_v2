#!/usr/bin/python3
"""Defines unnittests for models/amenity.py."""
import os
import models
import pep8
import unittest
import MySQLdb
from models.amenity import Amenity
from datetime import datetime
from models.base_model import BaseModel
from models.base_model import Base
from models.engine.file_storage import FileStorage
from models.engine.db_storage import DBStorage
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import OperationalError


class TestAmenity(unittest.TestCase):
    """Unittests for testing the Amenity class."""

    @classmethod
    def classsetup(cls):
        """
        Amenity testing setup.

        Temporarile renamed file.json
        Resets FileStorage objects dictionary
        Created DBstorage, FileStorage, and Amenity instances for testing
        """
        try:
            os.rename("file.json", "tmp")
        except IOError:
            FileStorage._FileStorage__objects = {}
            cls.filestorage = FileStorage()
            cls.amenity = Amenity(name="The Andrew Lindburg treatment")
            if isinstance(models.storage, DBStorage):
                cls.dbstorage = DBStorage()
                Base.metadata.create_all(cls.dbstorage._DBStorage__engine)
                Session = sessionmaker(bind=cls.dbstorage._DBStorage__engine)
                cls.dbstorage._DBStorage__session = Session()

    @classmethod
    def classteardown(cls):
        """
        Amenity for testing teardown
        Restore original file.json
        Delete DBstorage FileStorage, and Amenity test instances.
        """
        try:
            os.remove("file.json")
        except IOError:
            pass
        try:
            os.rename("tmp", "file.json")
        except IOError:
            pass
        del cls.amenity
        del cls.filestorage
        if isinstance(models.storage, DBStorage):
            cls.dbstorage._DBStorage__session.close()
            del cls.dbstorage

    def pep8_test(self):
        """Test pep8 styling."""
        style = pep8.StyleGuide(quiet=True)
        q = style.check_files(["models/amenity.py"])
        self.assertEqual(q.total_errors, 0, "fix pep8")

    def testdocstrings(self):
        """Check for docstrings."""
        self.assertIsNotNone(Amenity.__doc__)

    def test_attributes(self):
        """Check for attributes."""
        u = Amenity(email="a", password="a")
        self.assertEqual(str, type(u.id))
        self.assertEqual(datetime, type(u.created_at))
        self.assertEqual(datetime, type(u.updated_at))
        self.assertTrue(hasattr(u, "__tablename__"))
        self.assertTrue(hasattr(u, "name"))
        self.assertTrue(hasattr(u, "place_amenities"))

    @unittest.skipIf(isinstance(models.storage, FileStorage), "Testing FileStorage")
    def test_email_not_nullable(self):
        """Test that email attribute is non-nullable."""
        with self.assertRaises(OperationalError):
            self.dbstorage._DBStorage__session.add(Amenity(password="a"))
            self.dbstorage._DBStorage__session.commit()
        self.dbstorage._DBStorage__session.rollback()
        with self.assertRaises(OperationalError):
            self.dbstorage._DBStorage__session.add(Amenity(email="a"))
            self.dbstorage._DBStorage__session.commit()

        def test_is_subclass(self):
            """Check Amenity is subclass of BaseModel"""
            self.assertTrue(issubclass(Amenity, BaseModel))

        def test_init(self):
            """Test initialization."""
            self.assertIsInstance(self.amenity, Amenity)

        def test_two_models_are_unique(self):
            """Test that different Amenity instances are unique."""
            us = Amenity(email="a", password="a")
            self.assertNotEqual(self.amenity.id, us.id)
            self.assertLess(self.amenity.created_at, us.created_at)
            self.assertLess(self.amenity.updated_at, us.updated_at)

        def test_init_args_kwargs(self):
            """Test initialization with args and kwargs."""
            dt = datetime.utcnow()
            st = Amenity("1", id="5", created_at=dt.isoformat())
            self.assertEqual(st.id, "5")
            self.assertEqual(st.created_at, dt)

        def test_str(self):
            """Test __str__ representation."""
            s = self.amenity.__str__()
            self.assertIn("[Amenity] ({})".format(self.amenity.id), s)
            self.assertIn("'id': '{}'".format(self.amenity.id), s)
            self.assertIn("'created_at': {}".format(
                repr(self.amenity.created_at)), s)
            self.assertIn("'updated_at': {}".format(
                repr(self.amenity.updated_at)), s)
            self.assertIn("'name': '{}'".format(self.amenity.name), s)

        @unittest.skipIf(isinstance(models.storage, DBStorage), "Testing DBStorage")
        def test_save_filestorage(self):
            """Test save method with FileStorage."""
            old = self.amenity.updated_at
            self.amenity.save()
            self.assertLess(old, self.amenity.updated_at)
            with open("file.json", "r") as f:
                self.assertIn("Amenity." + self.amenity.id, f.read())

        @unittest.skipIf(isinstance(models.storage, FileStorage), "Testing FileStorage")
        def test_save_dbstorage(self):
            """Test save method with DBStorage."""
            old = self.amenity.updated_at
            self.amenity.save()
            self.assertLess(old, self.amenity.updated_at)
            db = MySQLdb.connect(user="hbnb_test",
                                    passwd="hbnb_test_pwd",
                                    db="hbnb_test_db")
            cursor = db.cursor()
            cursor.execute("SELECT * \
                                    FROM `amenities` \
                                WHERE BINARY name = '{}'".
                            format(self.amenity.name))
            query = cursor.fetchall()
            self.assertEqual(1, len(query))
            self.assertEqual(self.amenity.id, query[0][0])
            cursor.close()

        def test_to_dict(self):
            """Test to_dict method."""
            amenity_dict = self.amenity.to_dict()
            self.assertEqual(dict, type(amenity_dict))
            self.assertEqual(self.amenity.id, amenity_dict["id"])
            self.assertEqual("Amenity", amenity_dict["__class__"])
            self.assertEqual(self.amenity.created_at.isoformat(),
                                     amenity_dict["created_at"])
            self.assertEqual(self.amenity.updated_at.isoformat(),
                                     amenity_dict["updated_at"])
            self.assertEqual(self.amenity.name, amenity_dict["name"])


if __name__ == "__main__":
    unittest.main()
