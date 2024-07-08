#!/usr/bin/python3
"""This module defines a class to store data with SQLAlchemy"""
import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session
import models
import models.base_model
from models.base_model import Base
import models.state
import models.city
import models.user
import models.place
import models.amenity
import models.review

classes = {"State": models.state.State,
           "City": models.city.City,
           "User": models.user.User,
           "Place": models.place.Place,
           "Amenity": models.amenity.Amenity,
           "Review": models.review.Review}


class DBStorage:
    """This class manages data storage for a SQL Database"""
    __engine = None
    __session = None

    def __init__(self):
        HBNB_MYSQL_USER = os.getenv('HBNB_MYSQL_USER')
        HBNB_MYSQL_PWD = os.getenv('HBNB_MYSQL_PWD')
        HBNB_MYSQL_HOST = os.getenv('HBNB_MYSQL_HOST')
        HBNB_MYSQL_DB = os.getenv('HBNB_MYSQL_DB')
        HBNB_ENV = os.getenv('HBNB_ENV', 'development')

        print(HBNB_MYSQL_HOST)
        print(HBNB_MYSQL_PWD)

        self.__engine = create_engine('mysql+mysqldb://{}:{}@{}/{}'.
                                      format(HBNB_MYSQL_USER,
                                             HBNB_MYSQL_PWD,
                                             HBNB_MYSQL_HOST,
                                             HBNB_MYSQL_DB))

        if os.getenv(HBNB_ENV) == 'test':
            Base.metadata.drop_all(self.__engine)

    def all(self, cls=None):
        """query on the current database session (self.__session)
        all objects depending of the class name (argument cls)"""
        objects = {}
        if cls is None:
            for cls_obj in classes:
                objs = self.__session.query(classes[cls_obj]).all()
                for obj in objs:
                    key = f"{obj.__class__.__name__}.{obj.id}"
                    objects[key] = obj
        else:
            objs = self.__session.query(cls).all()
            for obj in objs:
                key = f"{obj.__class__.__name__}.{obj.id}"
                objects[key] = obj
        return objects

    def new(self, obj):
        """add the object to the current database session"""
        self.__session.add(obj)

    def save(self):
        """commit all changes of the current database session"""
        self.__session.commit()

    def delete(self, obj=None):
        """delete from the current database session obj if not None"""
        if obj is not None:
            self.__session.delete(obj)

    def reload(self):
        Base.metadata.create_all(self.__engine)
        session_make = sessionmaker(bind=self.__engine, expire_on_commit=False)
        session = scoped_session(session_make)
        self.__session = session()

    def close(self):
        """
        calls remove() on private session attr (self.__session)
        OR close() on the class Session
        """
        self.__session.remove()
