import unittest
from app import create_app, db
from app.models import AuthorAccount, Story
from sqlalchemy.exc import IntegrityError
from flask import url_for
from datetime import datetime
from flask_testing import TestCase


class ContextTestCase(TestCase):
    render_templates = True

    def create_app(self):
        app = create_app("testing")
        app.config['PRESERVE_CONTEXT_ON_EXCEPTION'] = False
        return app

    def _pre_setup(self):
        self.app = create_app('testing')
        self.client = self.app.test_client()

    def __call__(self, result=None):
        try:
            self._pre_setup()
            super(ContextTestCase, self).__call__(result)
        finally:
            self._post_teardown()

    def _post_teardown(self):
        if getattr(self, '_ctx', None) and self._ctx is not None:
            self._ctx.pop()
            del self._ctx


class BaseTestCase(ContextTestCase):
    """
    Base test case for application
    """

    def setUp(self):
        self.app_context = self.app.app_context()
        self.app_context.push()
        self.db = db

        db.create_all()

        self.create_author_accounts()
        self.add_story()

        db.session.commit()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    @staticmethod
    def create_author_accounts():
        """
        Creates new users for testing follow feature
        :return: 2 new unique users to test follow and unfollow feature
        """

        author1 = AuthorAccount(first_name="test1", last_name="hadithi1",
                                username="test1hadithi", email="test1hadithi@hadithi.com",
                                password="password", registered_on=datetime.now())
        author2 = AuthorAccount(first_name="test", last_name="hadithi",
                                username="testhadithi", email="testhadithi@hadithi.com",
                                password="password", registered_on=datetime.now())

        author3 = AuthorAccount(first_name="Guy De", last_name="Maupassant",
                                username="guydemaupassant", email="guydemaupassant@hadithi.com",
                                password="password", registered_on=datetime.now())

        author4 = AuthorAccount(first_name="brian", last_name="lusina",
                                username="lusinabrian", email="lusinabrian@hadithi.com",
                                password="password", registered_on=datetime.now())

        try:
            db.session.add(author1)
            db.session.add(author2)
            db.session.add(author3)
            db.session.add(author4)
            db.session.commit()
        except IntegrityError as ie:
            print("Integrity Error: ", ie)
            db.session.rollback()

        return author1, author2, author3, author4

    def login(self):
        """
        Login in the user to the testing app
        :return: The authenticated user for the test app
        """
        return self.client.post(
            "auth/login",
            data=dict(email='guydemaupassant@hadithi.com', password='password', confirm='password'),
            follow_redirects=True
        )

    def add_story(self):
        """
        Adds a dummy story to the database
        :return:
        """
        author1, author2, author3, author4 = self.create_author_accounts()
        story = Story.query.filter_by(author_id=author1.id).first()
        if story is None:
            try:
                story = Story(title="Gotham in flames", tagline="Dark city catches fire",
                              category="Fiction", content="", author_id=author1.id)
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
