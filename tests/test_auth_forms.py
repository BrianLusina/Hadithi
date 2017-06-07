"""
Test cases for forms used in the application.
Ensure that the forms validate data before submission
"""
import unittest
from tests import BaseTestCase
from app.mod_auth.forms import RegisterForm, LoginForm, ForgotPassword


class TestRegisterForm(BaseTestCase):
    """
    Test Register form
    """

    def test_validate_success_register_form(self):
        """Test the correct data is validated"""
        form = RegisterForm(
            first_name="Janus",
            last_name="Cascade",
            username="janus",
            email="januscascade@hadithi.com",
            password="januscascade",
            verify_password="januscascade"
        )
        self.assertTrue(form.validate())

    def test_checks_for_invalid_password_lengths(self):
        """Tests for incorrect password lengths"""
        form = RegisterForm(
            first_name="Janus",
            last_name="Cascade",
            username="janus",
            email="januscascade@hadithi.com",
            password="janus",
            verify_password="janus"
        )
        self.assertFalse(form.validate())

    def test_validate_email_already_registered(self):
        """Tests that register form can't validate an email that already exists"""
        form = RegisterForm(
            first_name="Guy De",
            last_name="Maupassant",
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

    def test_correct_data_validates(self):
        """Test that correct data is validated"""
        login_form = LoginForm(email="guydemaupassant@hadithi.com", password="password")
        self.assertTrue(login_form.validate())

    def test_validate_invalid_email_format(self):
        """Test that the incorrect email format is not validated"""
        login_form = LoginForm(email="unknown", password="password")
        self.assertFalse(login_form.validate())


class TestForgotPasswordForm(BaseTestCase):
    """
    Test forgot password form
    """

    def test_validate_valid_email(self):
        """Test that forgot password checks for valid email address"""
        form = ForgotPassword(email="janus@hadithi.com")
        self.assertTrue(form.validate())

    def test_validate_invalid_email_format(self):
        """Test that invalid email format is not validated by form"""
        form = ForgotPassword(email="janus")
        self.assertFalse(form.validate())


if __name__ == "__main__":
    unittest.main()
