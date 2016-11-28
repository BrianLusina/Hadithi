import unittest
import uuid
from flask import current_app, url_for
from sqlalchemy.exc import IntegrityError
from app.models import Author, Story
from app import create_app, db

class ContextTestCase(unittest.TestCase):

    def __call__(self, result=None):
        try:
            self._pre_setup()
            super(ContextTestCase, self).__call__(result)
        finally:
            self.