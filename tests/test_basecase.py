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
            self._post_teardown()

    def _pre_setup(self):
        self.app = create_app('testing')
        self.client = self.app.test_client()
        self._ctx = self.app.test_request_context()
        self._ctx.push()

    def _post_teardown(self):
        if getattr(self, '_ctx') and self._ctx is not None:
            self._ctx.pop()
        del self._ctx
