#!/usr/bin/python3
"""Defines filestorage class"""
import json


class FileStorage:
    """
    Represents abtracted storage engine

    Attributes:
        __objects (dict): dictionary of instantiated obj
        __file_path (str): name of file to save objects to
    """

    __file_path = 'file.json'
    __objects = {}

    def all(self, cls=None):
        """
        Returns list: list of __object"""
        my_dict = {}
        if cls:
            for key, value in self.__objects.items():
                if key.startswith(str(cls.__name__)):
                    my_dict[key] = value
        else:
            my_dict = self.__objects
        return my_dict        

    def new(self, obj):
        """Adds new object to storage dictionary"""
        key = "{}.{}".format(type(obj).__name__, obj.id)
        self.__objects[key] = obj

    def save(self):
        """Saves storage dictionary to file"""
        with open(FileStorage.__file_path, 'w') as f:
            temp = {}
            for key, val in self.__objects.items():
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
            with open(FileStorage.__file_path, 'r') as f:
                temp = json.load(f)
                for key, val in temp.items():
                    self.__objects[key] = classes[val['__class__']](**val)
        except FileNotFoundError:
            pass

    def delete(self, obj=None):
        """Delete object from __objects if found"""
        if obj:
            key = "{}.{}".format(type(obj).__name__, obj.id)
            if key in self.__objects:
                del self.__objects[key]
                self.save()

    def close(self):
        """Call reload() to deserialize the JSON file to objects"""
        self.reload()
