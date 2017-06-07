import unittest
import uuid
from flask import current_app, url_for
from sqlalchemy.exc import IntegrityError
from app.mod_auth.models import AuthorAccount
from app.mod_story.models import Story
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


class BaseTestCase(ContextTestCase):
    """
    Base test case for Hadithi
    """
    def create_author_account(self):
        author = AuthorAccount.query.filter_by(email="johndoe@example.com").first()
        if author is None:
            try:
                author = AuthorAccount(fname="John", lname="Doe", email="johndoe@example.com", password="password")
                db.session.add(author)
            except IntegrityError as ie:
                print(ie)
                db.session.rollback()
        return author

    def add_story(self):
        author = self.create_author_account()
        story = Story.query.filter_by(author_id=author.id).first()
        if story is None:
            try:
                story = Story(title="Gotham in flames", tagline="Dark city catches fire", content="",
                              author_id=author.id, category="")
                db.session.add(story)
            except IntegrityError as e:
                print(e)
                db.session.rollback()
        return story

    def save_user_story(self, story_id):
        return self.client.get(
            url_for("story.save_story", app_id=story_id),
            follow_redirects=True)

    def setUp(self):
        db.create_all()

        self.create_author_account()
        self.add_story()

        db.session.commit()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
