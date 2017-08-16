import random
import string
from datetime import datetime


class Utils:
    @staticmethod
    def generate_url(length):
        return ''.join(
            random.choice(string.ascii_uppercase + string.ascii_lowercase + string.digits) for _ in range(length))

    @staticmethod
    def generate_timestamp():
        return datetime.timestamp(datetime.utcnow())

    @staticmethod
    def get_datetime():
        date = str(datetime.date(datetime.utcnow()))
        time = str(datetime.time(datetime.utcnow())).split('.')[0]
        return date + ' ' + time
