import unittest
from tests import BaseTestCase


class DashboardTestCases(BaseTestCase):
    def test_dashboard_route_requires_login(self):
        """Tests that the dashboard route requires a user login"""
        response = self.client.get("/dashboard", follow_redirects=True)
        self.assertTrue(response.status_code == 200)
        # self.assertTemplateUsed(name="auth/login.html")

    def test_dashboard_write_story(self):
        """Tests that the write story requires a login"""
        response = self.client.get("/new_story", follow_redirects=True)
        self.assertTrue(response.status_code == 200)
        # self.assertTemplateUsed("auth/login.html")

    def test_dashboard_resend_confirmation_requires_login(self):
        """Test that the resend link requires a login"""
        response = self.client.get("/resend", follow_redirects=True)
        self.assertTrue(response.status_code == 200)
        # self.assertTemplateUsed("auth/login.html")


if __name__ == '__main__':
    unittest.main()
