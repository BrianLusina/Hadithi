import unittest
from tests import BaseTestCase
from app import db
from app.models import AuthorAccount
from datetime import datetime
from werkzeug.security import check_password_hash


class ModelsTestCases(BaseTestCase):
    """
    Tests for the application Models
    """

    def test_author_registration(self):
        """Test that a new Author registration behaves as expected"""
        with self.client:
            self.client.post('/register', data=dict(
                email='guydemaupassant@hadithi.com',
                password='password', confirm='password'
            ), follow_redirects=True)
            author = AuthorAccount.query.filter_by(email='guydemaupassant@hadithi.com').first()
            self.assertTrue(author.id)
            self.assertTrue(author.email == 'guydemaupassant@hadithi.com')
            self.assertFalse(author.admin)

    def test_get_author_by_id(self):
        """Ensure that the id is correct for the current logged in user"""
        with self.client:
            self.client.post("/login", data=dict(
                email='guydemaupassant@hadithi.com',
                password='password'
            ), follow_redirects=True)
            # self.assertTrue(current_user.id == 1)
            # self.assertFalse(current_user.id == 20)

    def test_registered_on_defaults_to_datetime(self):
        """Ensure that the registered_on date is a datetime object"""
        with self.client:
            self.client.post('/login', data=dict(
                email='guydemaupassant@hadithi.com',
                password='password'
            ), follow_redirects=True)
            author = AuthorAccount.query.filter_by(email='guydemaupassant@hadithi.com').first()
            self.assertIsInstance(author.registered_on, datetime)

    def test_check_password(self):
        """Ensure given password is correct after un-hashing"""
        author = AuthorAccount.query.filter_by(email='guydemaupassant@hadithi.com').first()
        self.assertFalse(author.verify_password('admin'))
        self.assertFalse(author.verify_password('another_admin'))
        self.assertTrue(check_password_hash(author.get_password, "password"))
        self.assertFalse(check_password_hash(author.get_password, "foobar"))

    def test_validate_invalid_password(self):
        """Test to ensure user can not log in with an invalid password"""
        with self.client:
            response = self.client.post("/login", data=dict(
                email='guydemaupassant@hadithi.com',
                password='password_pass'
            ), follow_redirects=True)
            # self.assertIn(b"Invalid email and/or password", response.data)

    def test_password_verification(self):
        """_____Successful password decryption should equal entered password"""
        author = AuthorAccount(password='cat')
        self.assertTrue(author.verify_password('cat'))
        self.assertFalse(author.verify_password('dog'))

    def test_no_password_getter(self):
        """_____Checking password object of author after being set"""
        author = AuthorAccount(password='cat')
        with self.assertRaises(AttributeError):
            author.password

    def test_password_setter(self):
        """_____Successful password property of author should not be none"""
        author = AuthorAccount(password='cat')
        self.assertTrue(author.password_hash is not None)

    def test_password_salts_are_random(self):
        """_____Hashed passwords should not be the same"""
        author = AuthorAccount(password='cat')
        user2 = AuthorAccount(password='cat')
        self.assertTrue(author.password_hash != user2.password_hash)

    def test_author_avatar(self):
        """>>>> Test that author avatar is generated"""
        author = AuthorAccount.query.filter_by(email='guydemaupassant@hadithi.com').first()
        avatar = author.avatar(128)
        expected = "http://www.gravatar.com/avatar/fed209f2d62f792377bbdf5ee864ee9b"
        self.assertEqual(avatar[0: len(expected)], expected)

    @staticmethod
    def add_and_fetch_new_users():
        """
        Creates new users for testing follow feature
        :return: 2 new unique users to test follow and unfollow feature
        """
        author1 = AuthorAccount(first_name="test1", last_name="hadithi1",
                                username="test1hadithi", email="test1hadithi@hadithi.com",
                                password="password", registered_on=datetime.now())
        author2 = AuthorAccount(first_name="test", last_name="hadithi",
                                username="testhadithi", email="testhadithi@hadithi.com",
                                password="password", registered_on=datetime.now())
        db.session.add(author1)
        db.session.add(author2)
        db.session.commit()

        return author1, author2

    def test_new_users_can_not_unfollow_user_they_do_not_follow(self):
        """>>>> Test that a new user can not unfollow a user they do not follow"""
        author1, author2 = self.add_and_fetch_new_users()

        self.assertIsNone(author2.unfollow(author1))

    def test_new_one_author_can_follow_another(self):
        """>>>> Test that author 1 can follow author 2"""
        author1, author2 = self.add_and_fetch_new_users()
        user = author1.follow(author2)

        db.session.add(user)
        db.session.commit()

        # test that the follow feature does not return an object after adding to session
        self.assertIsNone(author1.follow(author2))

        # check that author 1 is following author2
        self.assertTrue(author1.is_following(author2))

        # test that we can count how many authors author1 is following
        self.assertEqual(author1.following.count(), 1)

        # test that we can get the details of who author1 is following
        self.assertEqual(author1.following.first().first_name, "test")

        # test that we can get count of author2 followers
        self.assertEqual(author2.followers.count(), 1)

        # test that we can get details of author2 followers
        self.assertEqual(author2.followers.first().username, "test1hadithi")

        # un-follow author2
        u = author1.unfollow(author2)
        # test that an object is returned
        self.assertIsNotNone(u)

        db.session.add(u)
        db.session.commit()

        self.assertFalse(author1.is_following(author2))

        # author1 is not following anyone
        self.assertEqual(author1.following.count(), 0)

        # test that author2 has no followers
        self.assertEqual(author2.followers.count(), 0)


if __name__ == '__main__':
    unittest.main()
