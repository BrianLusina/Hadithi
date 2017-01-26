from sqlalchemy import Column, String, Integer, DateTime, func, ForeignKey, Boolean
from sqlalchemy.orm import relationship
from abc import ABCMeta, abstractmethod
import uuid
from werkzeug.security import generate_password_hash, check_password_hash, gen_salt
from sqlalchemy.ext.declarative import declared_attr
from flask_login import UserMixin
from . import db, login_manager
from datetime import datetime


class Base(db.Model):
    """
    Base class where all tables inherit from
    """
    __metaclass__ = ABCMeta
    __abstract__ = True

    id = Column(Integer, primary_key=True, autoincrement=True)
    date_created = Column(DateTime, default=func.current_timestamp())
    date_modified = Column(DateTime, default=func.current_timestamp(), onupdate=func.current_timestamp())

    @abstractmethod
    def __repr__(self):
        """
        :return: representation of this object as a Human readable string
        """
        pass


class AuthorAccount(db.Model):
    """
    Will handle authentication book keeping for the author account
    :cvar author_account_id: author account id which is a Foreign key, relating to author profile
    :cvar username: Author's username
    :cvar email, author's email address
    :cvar password, the author's password
    :cvar password_salt, the password salt that will be added to the hash to increase security
    :cvar email_confirmation_token, author's confirmation token fo the email address
    :cvar account_status_id, status of the account
    :cvar admin, whether this user is an admin, default is false
    :cvar registered_on, date this account was registered
    :cvar confirmed, whether this identity has been verified by the user
    :cvar confirmed_on, the date this account was confirmed
    """
    __tablename = "author_account"

    author_account_id = Column(Integer, ForeignKey("author.id"), primary_key=True)
    uuid = Column(String(250), default=str(uuid.uuid4()), nullable=False)
    username = Column(String(250), nullable=False)
    email = Column(String(250), nullable=False, unique=True)
    admin = Column(Boolean, nullable=True, default=False)
    password = Column(String(500), nullable=False)
    password_salt = Column(String(500))
    email_confirmation_token = Column(String(500), nullable=False, default=None)
    account_status_id = Column(Integer)
    registered_on = Column(DateTime, nullable=False)
    confirmed = Column(Boolean, nullable=False, default=False)
    confirmed_on = Column(DateTime, nullable=True)

    def __repr__(self):
        pass


class Author(Base, UserMixin):
    """
    Table for authors of Hadithi
    Sets the properties for attributes that are sensitive to the user, their profile
    :cvar __tablename__ name of this table in the database
    :cvar uuid the unique user id, that will be auto generated
    :cvar full_name, the full name of the user
    :cvar email, the email of the user
    :cvar password_hash, the password that will be hashed and hidden from other users
    :cvar admin, whether this user is an admin, default is false
    :cvar registered_on, date this account was registered
    :cvar confirmed, whether this identity has been verified by the user
    :cvar confirmed_on, the date this account was confirmed
    """

    __tablename__ = "author"
    uuid = Column(String(250), default=str(uuid.uuid4()), nullable=False)
    full_name = Column(String(100), nullable=False)
    email = Column(String(250), nullable=False, unique=True)
    password_hash = Column(String(250), nullable=False)
    admin = Column(Boolean, nullable=True, default=False)
    registered_on = Column(DateTime, nullable=False)
    confirmed = Column(Boolean, nullable=False, default=False)
    confirmed_on = Column(DateTime, nullable=True)

    @property
    def registered(self):
        return self.registered_on

    @registered.setter
    def registered(self):
        self.registered_on = datetime.now()

    @property
    def password(self):
        raise AttributeError("Password is not a readable attribute")

    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)

    @password.getter
    def get_password(self):
        return self.password_hash

    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return "<UserId:%r Name :%r, Email: %r>" % (self.uuid, self.full_name, self.email)


# This callback is used to reload the user object from the user ID stored in the session
@login_manager.user_loader
def load_author(user_id):
    return Author.query.get(int(user_id))


class ExternalServiceAccount(db.Model):
    """
    Abstract class that will superclass all external service accounts,
    """
    __metaclass__ = ABCMeta
    __abstract__ = True

    @declared_attr
    def author_profile_id(self):
        return Column(Integer, ForeignKey("author_account.author_account_id"), primary_key=True)


class FacebookAccount(ExternalServiceAccount):
    """
    Facebook account details for the author
    :cvar __tablename__: name of this table as represented in the database
    :cvar facebook_id: Facebook id received from
    """
    __tablename__ = "facebook_account"
    facebook_id = Column(String(100), nullable=True)


class TwitterAccount(ExternalServiceAccount):
    """
    Twitter account table
    :cvar __tablename__: table name as rep in database
    :cvar twitter_id: The twitter id as set in Twitter, or as received from Twitter
    """
    __tablename__ = "twitter_account"
    twitter_id = Column(String(100), nullable=True)


class GoogleAccount(ExternalServiceAccount):
    """
    Google Account table
    :cvar __tablename__: name of table in database
    :cvar google_id: Google id as received from Google on registration
    """
    __tablename__ = "google_account"
    google_id = Column(String(100), nullable=True)


class Story(Base):
    """
    Story table. Contains all the stories in the database
    :cvar __tablename__ Name of class as a table in SQL db
    """

    __tablename__ = 'story_table'

    title = Column(String, nullable=False)
    tagline = Column(String(50), default=title)
    category = Column(String(100), default="Other")
    content = Column(String(10000), nullable=False)
    author_id = Column(Integer, ForeignKey('author.id'))

    author = relationship(Author)

    def __init__(self, title, tagline, category, content, author_id):
        """
        :param title: Title of this story in the database
        :param tagline: Tagline of this story
        :param content: Content of this story
        :param author_id: The author id of whoever wrote this story
        """
        self.title = title
        self.tagline = tagline
        self.category = category
        self.content = content
        self.author_id = author_id

    def __repr__(self):
        return "Story: <Title: %r, Category: %r, Tagline: %r> AuthorId: %r" % \
               (self.title, self.category, self.tagline, self.author_id)
