#!/usr/bin/python3
""" Place Module for HBNB project """
from models.base_model import BaseModel, Base
import os
from sqlalchemy import Column, Integer, Float, Text, String, ForeignKey, Table
from sqlalchemy.orm import relationship

if os.getenv('HBNB_TYPE_STORAGE') == 'db':
    place_amenity = Table('place_amenity',
                          Base.metadata,
                          Column('place_id',
                                 String(60),
                                 ForeignKey('places.id'),
                                 primary_key=True),
                          Column('amenity_id',
                                 String(60),
                                 ForeignKey('amenities.id'),
                                 primary_key=True))


class Place(BaseModel, Base):
    """ A place to stay """
    __tablename__ = 'places'
    if os.getenv('HBNB_TYPE_STORAGE') == 'db':
        city_id = Column(String(60), ForeignKey('cities.id'), nullable=False)
        user_id = Column(String(60), ForeignKey('users.id'), nullable=False)
        name = Column(String(128), nullable=False)
        description = Column(String(1024), nullable=True)
        number_rooms = Column(Integer, nullable=False, default=0)
        number_bathrooms = Column(Integer, nullable=False, default=0)
        max_guest = Column(Integer, nullable=False, default=0)
        price_by_night = Column(Integer, nullable=False, default=0)
        latitude = Column(Float, nullable=True)
        longitude = Column(Float, nullable=True)
        amenity_ids = Column(Text, nullable=True)
        reviews = relationship('Review', backref='place', cascade='delete')
        amenities = relationship('Amenity', secondary=place_amenity, backref='places')
    else:
        city_id = ""
        user_id = ""
        name = ""
        description = ""
        number_rooms = 0
        number_bathrooms = 0
        max_guest = 0
        price_by_night = 0
        latitude = 0.0
        longitude = 0.0
        amenity_ids = []

    def __init__(self, *args, **kwargs):
        """Initializes user"""
        super().__init__(*args, **kwargs)

    @property
    def reviews(self):
        import models
        from models.review import Review
        list_reviews = []
        all_reviews = models.storage.all(Review)
        for review in all_reviews.values():
            if review.place_id == self.id:
                list_reviews.append(review)
        return list_reviews
    
    @property
    def amenities(self):
        import models
        from models.amenity import Amenity
        list_amenities = []
        for amenity in models.storage.all(Amenity).values():
            if amenity.place_id == self.id:
                list_amenities.append(amenity)
        return list_amenities
