#!/usr/bin/python
'''
Read class level docstring
'''
import random
import string
from datetime import datetime


class Utils(object):
    '''
    Utility methods
    '''

    def __init__(self):
        pass

    @staticmethod
    def generate_url(length):
        '''
        Generates a random url for each post
        '''
        return ''.join(
            random.choice(
                string.ascii_uppercase + string.ascii_lowercase + string.digits
            ) for _ in range(length))

    @staticmethod
    def generate_timestamp():
        '''
        Generates a timestamp to be appended to posts
        '''
        return datetime.timestamp(datetime.utcnow())

    @staticmethod
    def get_datetime():
        '''
        Returns the current date and time
        '''
        date = str(datetime.date(datetime.utcnow()))
        time = str(datetime.time(datetime.utcnow())).split('.')[0]
        return date + ' ' + time
