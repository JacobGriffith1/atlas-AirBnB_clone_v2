#!/usr/bin/python3
"""This module instantiates an object of class FileStorage"""
from models.engine.file_storage import FileStorage
import os
import os

HBNB_TYPE_STORAGE = os.getenv("HBNB_TYPE_STORAGE")
if HBNB_TYPE_STORAGE == "db":
    from models.engine.db_storage import DBStorage
    storage = DBStorage()
    storage.reload()
else:
    storage = FileStorage()
    storage.reload()
