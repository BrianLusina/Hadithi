from sqlalchemy import Column, String, Integer, DateTime, func, ForeignKey
from sqlalchemy.orm import relationship
from abc import ABCMeta, abstractmethod
import uuid
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from . import db, login_manager


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


class Author(Base, UserMixin):
    """
    Table for authors of Hadithi
    :cvar __tablename__ name of this table in the database
    """
    __tablename__ = "author"
    uuid = Column(String(250), default=str(uuid.uuid4()), nullable=False)
    fname = Column(String(100), nullable=False)
    lname = Column(String(100), nullable=False)
    email = Column(String(250), nullable=False, unique=True)
    password_hash = Column(String(250), nullable=False)

    def __init__(self, fname, lname, email, password):
        self.fname = fname
        self.lname = lname
        self.email = email
        self.password_hash = password

    @property
    def password(self, password):
        raise AttributeError("Password is not a readable attribute")

    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return "<User:%r Name :%r %r, Email: %r>" % (self.uuid, self.fname, self.lname, self.email)


class Story(Base):
    """
    Story table. Contains all the stories in the database
    :cvar __tablename__ Name of class as a table in SQL db
    """

    __tablename__ = 'story_table'

    title = Column(String, nullable=False)
    tagline = Column(String(50), )
    content = Column(String(1500), nullable=False)
    author_id = Column(Integer, ForeignKey('author.id'))

    author = relationship(Author)

    def __init__(self, title, tagline, content, author_id):
        """
        :param title: Title of this story in the database
        :param tagline: Tagline of this story
        :param content: Content of this story
        :param author_id: The author id of whoever wrote this story
        """
        self.title = title
        self.tagline = tagline
        self.content = content
        self.author_id = author_id

    def __repr__(self):
        return "Story: <Title: %r, Tagline: %r> AuthorId: %r" % (self.title, self.tagline, self.author_id)
