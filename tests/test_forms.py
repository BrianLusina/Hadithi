"""
Test cases for forms used in the application.
Ensure that the forms validate data before submission
"""
import unittest
from tests import BaseTestCase
from app.forms import RegisterForm, LoginForm, ForgotPassword, ContactForm, StoryForm, EditProfileForm
from string import ascii_letters


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

    def test_validates_empty_fields(self):
        """Tests to check that empty fields are not submitted"""
        form = StoryForm(
            story_title="",
            tagline="Did you hear that?",
            category="",
            content="Some long story here"
        )
        self.assertFalse(form.validate())

    # todo: add tests for saving as a draft


class TestEditProfileForm(BaseTestCase):
    """
    Tests for the edit profile form
    """
    def test_validates_length_of_form(self):
        """>>>> Test that the edit profile form about me section is no more than 250 characters"""

        form = EditProfileForm(new_email=self.test_author_email, new_username=self.test_author_username,
                               about_me=ascii_letters * 5)
        self.assertFalse(form.validate_on_submit())

    def test_validates_length_of_about_me(self):
        """>>>> Test that the edit profile form allows for valid about me posts"""
        form = EditProfileForm(new_email=self.test_author_email, new_username=self.test_author_username,
                               about_me=ascii_letters * 4)
        self.assertTrue(form.validate)

    def test_validate_user_can_not_edit_existing_usernama(self):
        """>>>> Test the user can not register with an already taken username"""
        form = EditProfileForm(new_email=self.test_author_email, new_username=self.test_author2_username,
                               about_me=ascii_letters * 4)
        self.assertFalse(form.validate)


if __name__ == "__main__":
    unittest.main()
