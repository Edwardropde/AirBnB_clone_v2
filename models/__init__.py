#!/usr/bin/python3
"""
Instantiates storage object

instantiates a database storage engine (DBStorage) if environmental
variable HBNB_TYPE_STORAGE is set to db
else instantiates file storage engine FileStorage
"""
from os import getenv


hbnb_type_storage = getenv('HBNB_TYPE_STORAGE')


if hbnb_type_storage == 'db':
    from models.engine.db_storage import DBStorage
    storage = DBStorage()
else:
    from models.engine.file_storage import FileStorage
    storage = FileStorage()

storage.reload()
