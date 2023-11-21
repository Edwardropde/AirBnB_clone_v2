#!/usr/bin/python3
"""Defines filestorage class"""
import json
from models.base_model import BaseModel
from models.user import User
from models.amenity import Amenity
from models.state import State
from models.city import City
from models.review import Review
from models.place import Place


class FileStorage:
    """
    Represents abtracted storage engine

    Attributes:
        __objects (dict): dictionary of instantiated obj
        __file_path (str): name of file to save objects to
    """

    __objects = {}
    __file_path = "file.json"

    def all(self, cls=None):
        """
        Returns dictionary of instantiated objects in __objects.
        """
        if cls is not None:
            if isinstance(cls, str):
                cls = eval(cls)
            cls_dict = {}
            for g, h in self.__objects.items():
                if isinstance(h, cls):
                    cls_dict[g] = h
            return cls_dict
        return self.__objects

    def new(self, obj):
        """Set in __objects obj using the key <obj_class_name>.id."""
        self.__objects["{}.{}".format(type(obj).__name__, obj.id)] = obj

    def save(self):
        """Serialize __objects to the JSON file __file_path."""
        odict = {o: self.__objects[o].to_dict() for o in self.__objects.keys()}
        with open(self.__file_path, "w", encoding="utf-8") as f:
            json.dump(odict, f)

    def reload(self):
        """Deserialize the JSON file __file_path to __objects, if it exists."""
        try:
            with open(self.__file_path, "r", encoding="utf-8") as f:
                for o in json.load(f).values():
                    name = o["__class__"]
                    del o["__class__"]
                    self.new(eval(name)(**o))
        except FileNotFoundError:
            pass

    def delete(self, obj=None):
        """Delete obj from __objects if it exists."""
        if obj is not None:
            key = "{}.{}".format(type(obj).__name__, obj.id)
            if key in self.__objects:
                del self.__objects[key]
                self.save()
