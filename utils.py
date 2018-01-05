#!/usr/bin/python
"""
Read class level docstring
"""
import random
import string
from datetime import datetime

from yaml import load


class Utils(object):
    """
    Utility methods
    """

    def __init__(self):
        pass

    @staticmethod
    def generate_url(length):
        """
        Generates a random url for each post
        """
        return ''.join(
            random.choice(
                string.ascii_uppercase + string.ascii_lowercase + string.digits
            ) for _ in range(length))

    @staticmethod
    def generate_timestamp():
        """
        Generates a timestamp to be appended to posts
        """
        return datetime.timestamp(datetime.utcnow())

    @staticmethod
    def get_datetime():
        """
        Returns the current date and time
        """
        date = str(datetime.date(datetime.utcnow()))
        time = str(datetime.time(datetime.utcnow())).split('.')[0]
        return date + ' ' + time

    @staticmethod
    def generate_validation_url(life=1440):
        """
        Generates a url that the registered_user can use to validate and active their account
        :param: life - This is the life of the url in minutes, after this the url will not be valid,
                        and the registered_user will need to start the registration process again
        """


class Config:
    def __init__(self, filename='config.yml'):
        self.filename = filename
        self.conf = None

    def load_config(self):
        with open(self.filename, 'r') as conf:
            self.conf = load(conf)

    def get(self, key=None):
        """
        Get a value from configuration object
        """
        if key is None:
            return None
        else:
            return self.conf[key]

    def set(self, key, value):
        """
        Add a key to the configuration options.
        Possible this will never be used
        """
        pass
