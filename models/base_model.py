#!/usr/bin/python3
"""This module defines a base class for all models in our hbnb clone"""
import uuid
import models
from datetime import datetime
from sqlalchemy.ext.declarative import declarative_base


Base = declarative_base()


class BaseModel:
    """A base class for all hbnb models"""

    # Add or replace in class BaseModel:

    # class attribute id
        # represents a column containing a unique string (60 chars)
        # can't be null
        # primary key
    # class attribute created_at
        # represents a column containing a datetime
        # can't be null
        # default value is the current datetime ("datetime.utcnow()")
    # class attribute updated_at
        # represents a column containing a datetime
        # can't be null
        # default value is the current datetime ("datetime.utcnow()")

    def __init__(self, *args, **kwargs):
        """Instatntiates a new model"""
        if not kwargs:
            from models import storage
            self.id = str(uuid.uuid4())
            self.created_at = datetime.now()
            self.updated_at = datetime.now()
        else:
            if not kwargs.get('updated_at'):
                kwargs['updated_at'] = datetime.utcnow()
            else:
                kwargs['updated_at'] = datetime.strptime(kwargs['updated_at'],
                                                         '%Y-%m-%dT%H:%M:%S.%f')

            if not kwargs.get('created_at'):
                kwargs['created_at'] = datetime.utcnow()
            else:
                kwargs['created_at'] = datetime.strptime(kwargs['created_at'],
                                                         '%Y-%m-%dT%H:%M:%S.%f')

            if kwargs.get('__class__'):
                del kwargs['__class__']

            self.id = kwargs.get('id') or str(uuid.uuid4())

            self.__dict__.update(kwargs)

    def __str__(self):
        """Returns a string representation of the instance"""
        cls = (str(type(self)).split('.')[-1]).split('\'')[0]
        return '[{}] ({}) {}'.format(cls, self.id, self.__dict__)

    def save(self):
        """Updates updated_at with current time when instance is changed"""
        from models import storage
        self.updated_at = datetime.utcnow()
        storage.new(self)
        storage.save()

    def to_dict(self):
        """Convert instance into dict format"""
        dictionary = {}
        dictionary.update(self.__dict__)
        dictionary.update({'__class__':
                          (str(type(self)).split('.')[-1]).split('\'')[0]})
        dictionary['created_at'] = self.created_at.isoformat()
        dictionary['updated_at'] = self.updated_at.isoformat()
        if '_sa_instance_state' in dictionary:
            del dictionary['_sa_instance_state']
        return dictionary
    
    def delete(self):
        """deletes an instance based on class name and id"""
        from models import storage
        storage.delete(self)
