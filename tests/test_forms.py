import unittest
from tests import BaseTestCase
from app.forms import RegisterForm, LoginForm, ForgotPassword, ContactForm, StoryForm


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


class TestContactForm(BaseTestCase):
    """
    Tests for the contact form
    """

    def test_validate_all_fields_are_filled(self):
        """Tests to check data is not submitted with empty fields"""
        form = ContactForm(
            sender_name="Virginia",
            sender_email="virginia@gmail.com",
            sender_message="Some long message"
        )
        self.assertTrue(form.validate())

    def test_validate_invalid_data_is_not_submitted(self):
        """Test that the contact form does not take empty fields"""
        form = ContactForm(
            sender_name="",
            sender_email="virginia@gmail.com",
            sender_message="Some long message"
        )
        self.assertFalse(form.validate())

    def test_validate_invalid_email_format_is_not_submitted(self):
        """Test that the contact form does not take empty fields"""
        form = ContactForm(
            sender_name="Virginia",
            sender_email="virginia",
            sender_message="Some long message"
        )
        self.assertFalse(form.validate())

    def test_validate_empty_message_is_not_submitted(self):
        """Test that the contact form does not take empty fields"""
        form = ContactForm(
            sender_name="",
            sender_email="virginia@gmail.com",
            sender_message=""
        )
        self.assertFalse(form.validate())


class TestStoryForm(BaseTestCase):
    """
    Tests for The Story form
    """

    def test_validates_story_form_data(self):
        """Test to check that all fields are filled"""
        form = StoryForm(
            story_title="The Whisper",
            tagline="Did you hear that?",
            category="Fiction",
            content="Some long story here"
        )
        self.assertTrue(form.validate())


if __name__ == "__main__":
    unittest.main()
