from sqlalchemy import Column, String, Integer, ForeignKey
from app.models import Base


class Story(Base):
    """
    Story table. Contains all the stories in the database
    :cvar __tablename__ Name of class as a table in SQL db
    """

    __tablename__ = 'story'

    title = Column(String, nullable=False)
    tagline = Column(String(50), default=title)
    category = Column(String(100), default="Other")
    content = Column(String(10000), nullable=False)
    author_id = Column(Integer, ForeignKey("author.id"))

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
