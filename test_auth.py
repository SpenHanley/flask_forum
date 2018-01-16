import unittest
import os
import json
from app import create_app, db


class AuthTestCase(unittest.TestCase):
    """ This class represents the authenticated test case """

    def setUp(self):
        """ Define test variables and initialise app """
        self.app = create_app(config_name='testing')
        self.client = self.app.test_client
        self.post = {'':'','':''}
