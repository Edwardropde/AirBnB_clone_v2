#!/usr/bin/python3
"""
Instantiates storage object

instantiates a database storage engine (DBStorage) if environmental
variable HBNB_TYPE_STORAGE is set to db
else instantiates file storage engine FileStorage
"""
import os

from models.engine.db_storage import DBStorage
from models.engine.file_storage import FileStorage

storage = DBStorage() if os.getenv('HBNB_TYPE_STORAGE') == 'db' else FileStorage()
storage.reload()
