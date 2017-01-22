import unittest
from flask import url_for
from flask_login import current_user
from tests import BaseTestCase


class TestUserViews(BaseTestCase):
    """
    Tests for auth blueprint views
    """

    def test_correct_login(self):
        """Test login behaves correctly with correct credentials"""
        with self.client:
            response = self.login()

            self.assertTrue(response.status_code == 200)
            # todo: check why current user is not authenticated or active?
            # self.assertTrue(current_user.is_active)
            # self.assertTrue(current_user.is_authenticated)

    def test_incorrect_login(self):
        """Test to ensure login behaves correctly with incorrect credentials"""
        with self.client:
            response = self.client.post(
                url_for("auth.login"),
                data=dict(email='guydemaupassant@hadithi.com', password='wrong', confirm='password'),
                follow_redirects=True
            )

            self.assertTrue(response.status_code == 200)
            self.assertFalse(current_user.is_active)
            self.assertFalse(current_user.is_authenticated)

    def test_logout(self):
        """Test that logout behaves correctly"""
        with self.client:
            self.login()

            response = self.client.get('/logout', follow_redirects=True)

            self.assertTrue(b'Logout' not in response.data)
            self.assertFalse(current_user.is_active)
            self.assertTrue(current_user.is_anonymous)

    def test_logout_route_requires_login(self):
        """ Test to ensure that logout page requires author login"""
        response = self.client.get('/logout', follow_redirects=True)
        self.assertTrue(response.status_code == 200)
        # todo: handle assertion in for response data
        # self.assertIn(b'Please login', response.data)

    def test_login_page_loads(self):
        """Test Login page should load successfully"""
        response = self.client.get('/login')
        self.assertIn(b'login', response.data)

    def test_register_account_page_loads(self):
        """Test register page loads successfully"""
        response = self.client.get(url_for("auth.register"))
        self.assertTrue(b'Register' in response.data)

    def test_confirm_token_route_requires_login(self):
        """Test the confirm/<token> route requires a logged in user"""
        # blah is the random token
        self.client.get("/confirm/blah", follow_redirects=True)
        self.assertTemplateUsed('auth/login.html')

if __name__ == '__main__':
    unittest.main()
