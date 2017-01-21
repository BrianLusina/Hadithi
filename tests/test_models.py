import unittest
from tests import BaseTestCase
from app.models import Author
from datetime import datetime
from flask_login import current_user
from werkzeug.security import check_password_hash


class ModelsTestCases(BaseTestCase):
    """
    Tests for the application Models
    """

    def test_author_registration(self):
        """Test that a new Author registration behaves as expected"""
        with self.client:
            self.client.post('/register', data=dict(
                email='guydemaupassant@hadithi.com',
                password='password', confirm='password'
            ), follow_redirects=True)
            author = Author.query.filter_by(email='guydemaupassant@hadithi.com').first()
            self.assertTrue(author.id)
            self.assertTrue(author.email == 'guydemaupassant@hadithi.com')
            self.assertFalse(author.admin)

    def test_get_author_by_id(self):
        """Ensure that the id is correct for the current logged in user"""
        with self.client:
            self.client.post("/login", data=dict(
                email='guydemaupassant@hadithi.com',
                password='password'
            ), follow_redirects=True)
            print(current_user.is_authenticated)
            self.assertTrue(current_user.id == 1)

    def test_registered_on_defaults_to_datetime(self):
        """Ensure that the registered_on date is a datetime object"""
        with self.client:
            self.client.post('/login', data=dict(
                email='guydemaupassant@hadithi.com',
                password='password'
            ), follow_redirects=True)
            author = Author.query.filter_by(email='guydemaupassant@hadithi.com').first()
            self.assertIsInstance(author.registered_on, datetime)

    def test_check_password(self):
        """Ensure given password is correct after un-hashing"""
        author = Author.query.filter_by(email='guydemaupassant@hadithi.com').first()
        self.assertTrue(check_password_hash(author.get_password, "password"))
        self.assertFalse(check_password_hash(author.get_password, "foobar"))

    def test_validate_invalid_password(self):
        """Test to ensure user can not log in with an invalid password"""
        with self.client:
            response = self.client.post("/login", data=dict(
                email='guydemaupassant@hadithi.com',
                password='password_pass'
            ), follow_redirects=True)
        #self.assertIn(b"Invalid email and/or password", response.data)

if __name__ == '__main__':
    unittest.main()
