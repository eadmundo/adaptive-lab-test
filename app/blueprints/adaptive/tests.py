import unittest

from app import create_app
from app.extensions.db import db

class AdaptiveTestCase(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.app = create_app(config='config/test.py')
        cls.app_test_client = cls.app.test_client()

    def test_main_page_loads(self):
        """Main page of application returns 200"""
        rv = self.app_test_client.get('/')
        self.assertEqual(rv.status_code, 200)

    @classmethod
    def tearDownClass(cls):
        pass
