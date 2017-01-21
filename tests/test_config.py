import unittest
from flask import current_app
from flask_testing import TestCase
from app import create_app


class TestConfigurationsCases(TestCase):
    """
    Test for configuration of the application. These Tests ensure that the testing configurations run
    as the should under TESTING config
    """

    def create_app(self):
        app = create_app("testing")
        return app

    def test_app_is_testing(self):
        """Test application can be configured for testing"""
        self.assertTrue(current_app.config["TESTING"])

    def test_app_is_debuggable(self):
        """Test application can be in debug mode"""
        self.assertTrue(current_app.config.get("DEBUG") is True)

    def test_app_has_wsrf_enabled(self):
        """Test application has WSRF disabled in testing mode"""
        self.assertTrue(current_app.config.get("WTF_CSRF_ENABLED") is False)

    def test_app_exists(self):
        """Test that the application exists"""
        self.assertFalse(current_app is None)

if __name__ == '__main__':
    unittest.main()
