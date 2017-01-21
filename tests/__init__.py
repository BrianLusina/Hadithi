import unittest
from app import create_app, db
from app.models import Author, Story
from sqlalchemy.exc import IntegrityError
from flask import url_for
from datetime import datetime


class ContextTestCase(unittest.TestCase):

    @staticmethod
    def create_app():
        app = create_app("testing")
        return app

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
    Base test case for application
    """

    def setUp(self):
        self.app_context = self.app.app_context()
        self.app_context.push()

        db.create_all()

        self.create_author_account()
        self.add_story()

        db.session.commit()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    @staticmethod
    def create_author_account():
        """
        Create a fictional Author for testing
        :return:
        """
        author = Author.query.filter_by(email="guydemaupassant@hadithi.com").first()
        if author is None:
            try:
                author = Author(full_name="Guy De Maupassant", email="guydemaupassant@hadithi.com",
                                password="password", registered_on=datetime.now())
                db.session.add(author)
            except IntegrityError as ie:
                print(ie)
                db.session.rollback()
        return author

    def add_story(self):
        """
        Adds a dummy story to the database
        :return:
        """
        author = self.create_author_account()
        story = Story.query.filter_by(author_id=author.id).first()
        if story is None:
            try:
                story = Story(title="Gotham in flames", tagline="Dark city catches fire",
                              category="Fiction", content="", author_id=author.id)
                db.session.add(story)
            except IntegrityError as e:
                print(e)
                db.session.rollback()
        return story

    def save_user_story(self, story_id):
        return self.client.get(
            url_for("story.save_story", app_id=story_id),
            follow_redirects=True)


if __name__ == "__main__":
    unittest.main()
