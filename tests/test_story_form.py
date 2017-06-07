"""
Test cases for forms used in the application.
Ensure that the forms validate data before submission
"""
import unittest
from tests import BaseTestCase
from app.mod_story.forms import StoryForm


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

if __name__ == "__main__":
    unittest.main()
