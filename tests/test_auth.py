import unittest
import uuid
from flask import url_for, request
from app.models import Author
from flask_login import current_user
from tests import BaseTestCase


class TestUserViews(BaseTestCase):
    """
    Tests for author blueprint views
    """
    def test_login_page_loads(self):
        """_____Login page should load successfully"""
        response = self.client.get('/login')
        self.assertIn(b'Please login', response.data)

    def test_create_account_page_loads(self):
        """_____Create account page loads successfully"""
        response = self.client.get(url_for("auth.create_account"))
        self.assertTrue(b'Create Account' in response.data)

    def test_create_developer_account_page_loads(self):
        """_____Create developer account page loads successfully"""
        response = self.client.get(url_for("auth.create_developer_account"))
        self.assertTrue(b'website' in response.data)

    def test_correct_login(self):
        """_____Ensure login behaves correctly with correct credentials"""
        with self.client:
            response = self.login('admin@cs.com', 'admin')

            self.assertIn(b'Logout', response.data)
            self.assertTrue(current_user.username == "admin")
            self.assertTrue(current_user.is_active)

    def test_incorrect_login(self):
        """_____Ensure login behaves correctly with incorrect credentials"""
        with self.client:
            response = self.login('wrong.com', 'wrong')
            self.assertIn(b'Please login', response.data)

    def test_logout(self):
        """_____Ensure logout behaves correctly"""
        with self.client:
            self.login('admin@cs.com', 'admin')

            response = self.client.get('/logout', follow_redirects=True)

            self.assertTrue(b'Logout' not in response.data)
            self.assertFalse(current_user.is_active)
            self.assertTrue(current_user.is_anonymous)

    def test_logout_route_requires_login(self):
        """_____Ensure that logout page requires author login"""
        response = self.client.get('/logout', follow_redirects=True)
        self.assertIn(b'Please login', response.data)


if __name__ == '__main__':
    unittest.main()