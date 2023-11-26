#!/usr/bin/python3
"""
Instantiates storage object

instantiates a database storage engine (DBStorage) if environmental
variable HBNB_TYPE_STORAGE is set to db
else instantiates file storage engine FileStorage
"""
from models.engine.file_storage import FileStorage


storage = FileStorage()
storage.reload()
