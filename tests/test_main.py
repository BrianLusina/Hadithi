# tests/test_main.py

import unittest
import uuid
import os
import shutil
import io
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

    def test_applications_page_loads(self):
        """_____Applications page loads successfully"""
        response = self.client.get(url_for("main.application"))
        self.assertTrue(b'Application Details' in response.data)

    def test_added_apps_are_displayed_in_home_page(self):
        """_____Added applications should be displayed on the home page"""
        app = self.add_application()
        response = self.client.get('/')
        self.assertTrue(app.name.encode() in response.data)

    def test_app_info_page(self):
        """_____Applications info page should load successfully"""
        app = self.add_application()
        assets = self.add_assets()

        response = self.client.get(url_for('main.app_info', app_uuid=app.uuid))
        self.assertTrue(app.name.encode() in response.data)
        self.assertTrue(app.uuid.encode() in response.data)

    def test_installed_apps_are_displayed(self):
        """_____Installed apps should be displayed in installed apps section"""
        app = self.add_application()
        response = self.install_app(app.uuid)
        self.assertIn(b'/launch_app?app_id=%s' % (str(app.uuid)), response.data)

    def test_app_categoty_page_loads(self):
        """_____Category page loads successfully"""
        response = self.client.get(url_for("main.category"))
        self.assertTrue(b'Category Description' in response.data)

    def test_added_categories_are_displayed(self):
        """_____Installed apps should be displayed in installed apps section"""
        category = self.add_category()
        response = self.client.get('/category')
        self.assertTrue(category.description.encode() in response.data)


if __name__ == '__main__':
    unittest.main()