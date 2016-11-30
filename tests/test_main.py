# tests/test_main.py

import unittest
from flask import url_for, request, current_app
from app.models import Story, Author
from tests.test_basecase import BaseTestCase


class TestMainModels(BaseTestCase):
    """
    Tests for main blueprint tables and models
    """
    def save_story(self, title, tagline, content, author_id):
        return self.client.post(
            url_for("main.application"),
            content_type='multipart/form-data',
            data=dict(title=title, tagline=tagline, content=content, author_id=author_id),
            follow_redirects=True)

    def save_category(self, name, description):
        return self.client.post(
            url_for("main.category"),
            data=dict(name=name, description=description),
            follow_redirects=True)

    def test_adding_new_stories(self):
        """_____Added application should be found in the database"""
        author = self.create_author_account()
        # category = self.add_category()

        with self.client:
            response = self.save_story(title="Great Stampede", tagline="Hooves and hoofs",
                                       content="Long time ago in distant",
                                       author_id=author.id)
            story = Story.query.filter_by(title='Great Stampede')
            story_count = story.count()

            self.assertTrue(story_count == 1)


class TestMainViews(BaseTestCase):
    """
    Tests for main blueprint views
    """
    def test_page_not_found(self):
        """_____Pages which dont exist should be directed to a 404 page"""
        response = self.client.get('/a-page-which-doesnt-exist')
        self.assertTrue(b'404' in response.data)

    def test_home_page_loads(self):
        """_____Home page should load successfully"""
        response = self.client.get('/')
        self.assertIn(b'Installed Apps', response.data)

    def test_nav_links_display_for_logged_in_users(self):
        """_____Navigation Links should display for logged in users"""
        self.login('admin@cs.com', 'admin')
        response = self.client.get('/')
        self.assertIn(b'Add Category', response.data)

    def test_no_nav_links_for_anonymous_users(self):
        """_____No navigation links for anonymous users"""
        response = self.client.get('/')
        self.assertTrue(b'Add Category' not in response.data)

    def test_added_stories_are_displayed_in_home_page(self):
        """_____Added stories should be displayed on the home page"""
        story = self.add_story()
        response = self.client.get('/')
        self.assertTrue(story.name.encode() in response.data)

    def test_story_detail_page(self):
        """_____Applications info page should load successfully"""
        story = self.add_story()

        response = self.client.get(url_for('story.detail', story_uuid=story.uuid))
        self.assertTrue(story.name.encode() in response.data)
        self.assertTrue(story.uuid.encode() in response.data)

    def test_saved_stories_are_displayed(self):
        """_____Saved stories should be saved in stories section"""
        story = self.add_story()
        response = self.save_user_story(story.uuid)
        self.assertIn(b'/story?story_id=%s' % (str(story.uuid)), response.data)

if __name__ == '__main__':
    unittest.main()
