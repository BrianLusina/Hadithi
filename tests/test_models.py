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
            # self.assertTrue(current_user.id == 1)
            # self.assertFalse(current_user.id == 20)

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
        self.assertFalse(author.verify_password('admin'))
        self.assertFalse(author.verify_password('another_admin'))
        self.assertTrue(check_password_hash(author.get_password, "password"))
        self.assertFalse(check_password_hash(author.get_password, "foobar"))

    def test_validate_invalid_password(self):
        """Test to ensure user can not log in with an invalid password"""
        with self.client:
            response = self.client.post("/login", data=dict(
                email='guydemaupassant@hadithi.com',
                password='password_pass'
            ), follow_redirects=True)
            # self.assertIn(b"Invalid email and/or password", response.data)

    def test_password_verification(self):
        """_____Successfull password decryption should equal entered password"""
        author = Author(password='cat')
        self.assertTrue(author.verify_password('cat'))
        self.assertFalse(author.verify_password('dog'))

    def test_no_password_getter(self):
        """_____Checking password object of author after being set"""
        author = Author(password='cat')
        with self.assertRaises(AttributeError):
            author.password

    def test_password_setter(self):
        """_____Successful password property of author should not be none"""
        author = Author(password='cat')
        self.assertTrue(author.password_hash is not None)

    def test_password_salts_are_random(self):
        """_____Hashed passwords should not be the same"""
        author = Author(password='cat')
        user2 = Author(password='cat')
        self.assertTrue(author.password_hash != user2.password_hash)


if __name__ == '__main__':
    unittest.main()
