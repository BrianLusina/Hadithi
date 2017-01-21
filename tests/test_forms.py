import unittest
from tests import BaseTestCase
from app.forms import RegisterForm, LoginForm, ForgotPassword


class TestRegisterForm(BaseTestCase):
    """
    Test Register form
    """
    def test_validate_success_register_form(self):
        """Test the correct data is validated"""
        form = RegisterForm(
            full_name="Janus Cascade",
            username="janus",
            email="januscascade@hadithi.com",
            password="januscascade",
            verify_password="januscascade"
        )
        self.assertTrue(form.validate())

    def test_checks_for_invalid_password_lengths(self):
        """Tests for incorrect password lengths"""
        form = RegisterForm(
            full_name="Janus Cascade",
            username="janus",
            email="januscascade@hadithi.com",
            password="janus",
            verify_password="janus"
        )
        self.assertFalse(form.validate())

    def test_validate_email_already_registered(self):
        """Tests that register form can't validate an email that already exists"""
        form = RegisterForm(
            full_name="Guy De Maupassant",
            username="guydemaupassant",
            email="guydemaupassant@hadithi.com",
            password="password",
            verify_password="password"
        )
        self.assertFalse(form.validate_form())


class TestLoginForm(BaseTestCase):
    """
    Test Login form
    """


class TestForgotPasswordForm(BaseTestCase):
    """
    Test forgot password form
    """

if __name__ == "__main__":
    unittest.main()
