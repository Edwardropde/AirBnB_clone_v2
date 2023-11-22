#!/usr/bin/python3
"""Defines filestorage class"""
import json
import os
from models.base_model import BaseModel
from models.user import User
from models.amenity import Amenity
from models.state import State
from models.city import City
from models.review import Review
from models.place import Place
from importlib import import_module


class FileStorage:
    """
    Represents abtracted storage engine

    Attributes:
        __objects (dict): dictionary of instantiated obj
        __file_path (str): name of file to save objects to
    """

    __objects = {}
    __file_path = "file.json"

    def __init__(self):
        """Initializes a FileStorage instance"""
        self.model_classes = {
            'BaseModel': import_module('models.base_model').BaseModel,
            'User': import_module('models.user').User,
            'State': import_module('models.state').State,
            'City': import_module('models.city').City,
            'Amenity': import_module('models.amenity').Amenity,
            'Place': import_module('models.place').Place,
            'Review': import_module('models.review').Review
            }

    def all(self, cls=None):
        """
        Returns dictionary of instantiated objects in __objects.
        """
        if cls is None:
            return self.__objects
        else:
            filtered_dict = {}
            for key, value in self.__objects.items():
                if type(value) is cls:
                    filtered_dict[key] = value
            return filtered_dict
    def delete(self, obj=None):
        """Removes an object from the storage dictionary"""
        if obj is not None:
            obj_key = obj.to_dict()['__class__'] + '.' + obj.id
            if obj_key in self.__objects.keys():
                del self.__objects[obj_key]

    def new(self, obj):
        """Set in __objects obj using the key <obj_class_name>.id."""
        self.__objects.update({obj.to_dict()['__class__'] + '.' + obj.id: obj})

    def save(self):
        """Serialize __objects to the JSON file __file_path."""
        with open(self.__file_path, 'w') as file:
            temp = {}
            for key, val in self.__objects.items():
                temp[key] = val.to_dict()
            json.dump(temp, file)

    def reload(self):
        """Deserialize the JSON file __file_path to __objects, if it exists."""
        classes = self.model_classes
        if os.path.isfile(self.__file_path):
            temp = {}
            with open(self.__file_path, 'r') as file:
                temp = json.load(file)
                for key, val in temp.items():
                    self.all()[key] = classes[val['__class__']](**val)

    def close(self):
        """Closes the storage engine."""
        self.reload()
