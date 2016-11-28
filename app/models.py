from sqlalchemy import Column, String, Integer, DateTime, func, ForeignKey
from sqlalchemy.orm import relationship
from flask_sqlalchemy import SQLAlchemy
from abc import ABCMeta, abstractmethod

db = SQLAlchemy()


class Base(db.Model):
    """
    Base class where all tables inherit from
    """
    __metaclass__ = ABCMeta

    id = Column(Integer, primary_key=True, autoincrement=True)
    date_created = Column(DateTime, default=func.current_timestamp())
    date_modified = Column(DateTime, default=func.current_timestamp(), onupdate=func.current_timestamp())

    @abstractmethod
    def __init__(self):
        pass

    @abstractmethod
    def __repr__(self):
        """
        :return: representation of this object as a Human readable string
        """
        pass


class Author(Base):
    """
    Table for authors of Hadithi
    """
    __tablename__ = "author"

    fname = Column(String, nullable=False)
    lname = Column(String, nullable=False)
    email = Column(String, nullable=False, unique=True)
    password = Column(String, nullable=False)

    def __init__(self, fname, lname, email, password):
        super().__init__()
        self.fname = fname
        self.lname = lname
        self.email = email
        self.password = password

    def __repr__(self):
        return "<Name :%r %r, Email: %r>" % (self.fname, self.lname, self.email)


class Story(Base):
    """
    Story table. Contains all the stories in the database
    :cvar __tablename__ Name of class as a table in SQL db
    """

    __tablename__ = 'story_table'

    title = Column(String, nullable=False)
    tagline = Column(String, )
    content = Column(String, nullable=False)

    author = Column(Integer, ForeignKey('author.id'))
    author_id = relationship(Author)

    def __init__(self, title, tagline, content, author_id):
        """
        :param title: Title of this story in the database
        :param tagline: Tagline of this story
        :param content: Content of this story
        :param author_id: The author id of whoever wrote this story
        """
        super().__init__()
        self.title = title
        self.tagline = tagline
        self.content = content
        self.author_id = author_id

    def __repr__(self):
        return "Story: <Title: %r, Tagline: %r> AuthorId: %r" % (self.title, self.tagline, self.author_id)
