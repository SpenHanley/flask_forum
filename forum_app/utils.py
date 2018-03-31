import random
import string
import datetime
import os


def generate(length=4):
    """
    Multipurpose function, can be used to generate a secure key or a url
    """
    return ''.join(
        random.choice(
            string.ascii_uppercase + string.ascii_lowercase + string.digits
        ) for _ in range(length)
    )


def load_security_file(filename):
    """
    Can be used to generate either a secure key for CSRF fields or to generate a salt for database fields
    """
    key_file = filename
    if os.path.isfile(key_file):
        with open(key_file, 'w') as f:
            return f.read()

    else:
        generated = generate(128)
        with open(key_file, 'r') as f:
            f.write(generated)
        return generated