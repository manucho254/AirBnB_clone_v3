#!/usr/bin/python3
""" holds class User"""
import models
from models.base_model import BaseModel, Base

from os import getenv

import sqlalchemy
from sqlalchemy import Column, String
from sqlalchemy.orm import relationship


class User(BaseModel, Base):
    """Representation of a user """
    if models.storage_t == 'db':
        __tablename__ = 'users'
        email = Column(String(128), nullable=False)
        password = Column(String(128), nullable=False)
        first_name = Column(String(128), nullable=True)
        last_name = Column(String(128), nullable=True)
        places = relationship("Place", backref="user")
        reviews = relationship("Review", backref="user")

    else:
        email = ""
        password = ""
        first_name = ""
        last_name = ""

    def to_dict(self):
        """ Returns a dictionary containing
           all keys/values of the instance
        """
        time = "%Y-%m-%dT%H:%M:%S.%f"
        new_dict = self.__dict__.copy()

        if "created_at" in new_dict:
            new_dict["created_at"] = new_dict["created_at"].strftime(time)

        if "updated_at" in new_dict:
            new_dict["updated_at"] = new_dict["updated_at"].strftime(time)
        new_dict["__class__"] = self.__class__.__name__

        if "_sa_instance_state" in new_dict:
            del new_dict["_sa_instance_state"]

        if models.storage_t == "db":
            del new_dict["password"]

        return new_dict

    def __init__(self, *args, **kwargs):
        """initializes user"""
        super().__init__(*args, **kwargs)
