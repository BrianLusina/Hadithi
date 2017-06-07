from sqlalchemy import Column, String, Integer, DateTime,  ForeignKey, Boolean, Table
from sqlalchemy.orm import relationship, backref
from abc import ABCMeta
from hashlib import md5
import uuid
from werkzeug.security import generate_password_hash, check_password_hash
from sqlalchemy.ext.declarative import declared_attr
from flask_login import UserMixin
from app import db, login_manager
from datetime import datetime
from app.models import Base
from app.mod_story.models import Story


# This is not a model but an association table to allow for a many to many relationship
# where a user can have many followers and can follow many other users
followers = Table("followers",
                  db.metadata,
                  Column("follower_id", Integer, ForeignKey("author.id")),
                  Column("followed_id", Integer, ForeignKey("author.id"))
                  )


class AuthorAccount(Base, UserMixin):
    """
    Table for authors of Hadithi
    Sets the properties for attributes that are sensitive to the user, their profile

    We will be linking AuthorAccount instances to other AuthorAccount instances,
    so as a convention let's say that for a pair of linked users in this relationship the left side user
    is following the right side user. We define the relationship as seen from the left side entity with the
    name followed, because when we query this relationship from the left side we will get the list of
    followed users.

    :cvar __tablename__ name of this table in the database
    :cvar uuid the unique user id, that will be auto generated
    :cvar first_name, the first name of the user
    :cvar last_name, last name of user
    :cvar email, the email of the user
    :cvar username: Author's username
    :cvar password_hash, the password that will be hashed and hidden from other users
    :cvar admin, whether this user is an admin, default is false
    :cvar registered_on, date this account was registered
    :cvar confirmed, whether this identity has been verified by the user
    :cvar confirmed_on, the date this account was confirmed
    """

    __tablename__ = "author"
    id = Column(Integer, primary_key=True, autoincrement=True)
    uuid = Column(String(250), default=str(uuid.uuid4()), nullable=False)
    first_name = Column(String(100), nullable=False, index=True)
    last_name = Column(String(100), nullable=False, index=True)
    email = Column(String(250), nullable=False, unique=True, index=True)
    username = Column(String(250), nullable=False, unique=True, index=True)
    about_me = Column(String(250), nullable=True)
    last_seen = Column(DateTime)
    password_hash = Column(String(250), nullable=False)
    admin = Column(Boolean, nullable=True, default=False)
    registered_on = Column(DateTime, nullable=False)
    confirmed = Column(Boolean, nullable=False, default=False)
    confirmed_on = Column(DateTime, nullable=True)

    stories = relationship("Story", backref="author", lazy="dynamic")

    following = relationship("AuthorAccount",
                             secondary=followers,
                             primaryjoin=(followers.c.follower_id == id),
                             secondaryjoin=(followers.c.followed_id == id),
                             backref=backref("followers", lazy="dynamic"),
                             lazy="dynamic"
                             )

    def avatar(self, size):
        """
        responsible for getting a user avatar. will reduce load on server by getting avatar image from Gravatar
        This creates an md5 hash of the user email and then incorporates it into the specially crafted URL
        After the md5 of the email you can provide a number of options to customize the avatar.
        The d=mm determines what placeholder image is returned when a user does not have an Gravatar account.
        The mm option returns the "mystery man" image, a gray silhouette of a person.
        The s=N option requests the avatar scaled to the given size in pixels.
        More information -> https://en.gravatar.com/site/implement/images
        :param size: size of the image
        :return: link to user's avatar
        """
        return 'http://www.gravatar.com/avatar/%s?d=mm&s=%d' % (md5(self.email.encode("utf-8")).hexdigest(), size)

    def followed_stories(self):
        """
        This returns all the stories this Author is following
        Will fetch the posts and order them by the time the stories were created in descending order
        the join operation will create a temporary table with data from the followers and data from the
        story table and merge them based on whether the author id matches

        Filter will return only stories that this particular user follows

        after that we sort the results of the new temp table in descending order by time
        :return: All the stories this user follows, this is based on the authors this user follows
        """
        return Story.query.join(followers, (followers.c.followed_id == Story.author_id)).filter(
            followers.c.followed_id == self.id).order_by(Story.date_created.desc())

    def follow(self, user):
        """
        this has been structured such that it returns a new object or None if the operation fails
        Allows this Author to be able to follow another author
        :param user: Author to follow
        :return: object if the follow feature succeeds, None otherwise
        :rtype: AuthorAccount or None
        """
        if not self.is_following(user):
            self.following.append(user)
            return self

    def unfollow(self, user):
        """
        Author can be able to unfollow a user they follow. Will return None if this user does not follow
        ther user they would like to unfollow
        :param user: the user this user would like to unfollow
        :return: AuthorAccount object or None
        :rtype: AuthorAccount or None
        """
        if self.is_following(user):
            self.following.remove(user)
            return self

    def is_following(self, user):
        """
        We are taking the followed relationship query, which returns all the (follower, followed) pairs that
        have our user as the follower, and we filter it by the followed user.
        This is possible because the followed relationship has a lazy mode of dynamic,
        so instead of being the result of the query, this is the actual query object, before execution.
        The return from the filter call is the modified query, still without having executed. So we then call
        count() on this query, and now the query will execute and return the number of records found.
        If we get one, then we know a link between these two uses is already present.
        If we get none then we know a link does not exist.
        :param user: the user to check against this user
        :return: Whether there is a link between this user and the user to check whether they are following
        """
        return self.following.filter(followers.c.followed_id == user.id).count() > 0

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
        return "<UserId:%r Name :<%r %r>, Email: %r>" % (self.uuid, self.first_name, self.last_name,
                                                         self.email)


# This callback is used to reload the user object from the user ID stored in the session
@login_manager.user_loader
def load_author(user_id):
    return AuthorAccount.query.get(int(user_id))


class ExternalServiceAccount(db.Model):
    """
    Abstract class that will superclass all external service accounts,

    :cvar first_name: first name as received from the external service account
    :cvar last_name: last name as received from external service account
    """
    __metaclass__ = ABCMeta
    __abstract__ = True

    first_name = Column(String(250), nullable=False)
    last_name = Column(String(250), nullable=False)
    email = Column(String(250), nullable=False)

    def __init__(self, email, first_name, last_name):
        self.email = email
        self.first_name = first_name
        self.last_name = last_name

    @declared_attr
    def author_id(self):
        """
        This is a declared attr, that will be used in all external accounts
        :return: Author profile id that is a foreign and primary key
        """
        return Column(Integer, ForeignKey(AuthorAccount.id), primary_key=True)


class FacebookAccount(ExternalServiceAccount):
    """
    Facebook account details for the author
    :cvar __tablename__: name of this table as represented in the database
    :cvar facebook_id: Facebook id received from
    """
    __tablename__ = "facebook_account"
    facebook_id = Column(String(100), nullable=True, unique=True)

    def __init__(self, facebook_id, email, first_name, last_name):
        super().__init__(email, first_name, last_name)
        self.facebook_id = facebook_id


class TwitterAccount(ExternalServiceAccount):
    """
    Twitter account table
    :cvar __tablename__: table name as rep in database
    :cvar twitter_id: The twitter id as set in Twitter, or as received from Twitter
    """
    __tablename__ = "twitter_account"
    twitter_id = Column(String(100), nullable=True, unique=True)

    def __init__(self, twitter_id, email, first_name, last_name):
        super().__init__(email, first_name, last_name)
        self.twitter_id = twitter_id


class GoogleAccount(ExternalServiceAccount):
    """
    Google Account table
    :cvar __tablename__: name of table in database
    :cvar google_id: Google id as received from Google on registration
    """
    __tablename__ = "google_account"
    google_id = Column(String(100), nullable=True, unique=True)

    def __init__(self, google_id, email, first_name, last_name):
        super().__init__(email, first_name, last_name)
        self.google_id = google_id


class AsyncOperationStatus(Base):
    """
    Dictionary table that stores 3 available statuses, pending, ok, error
    """
    __tablename__ = "async_operation_status"

    code = Column("code", String(20), nullable=True)

    def __repr__(self):
        pass


class AsyncOperation(Base):
    """

    """
    __tablename__ = "async_operation"

    async_operation_status_id = Column(Integer, ForeignKey(AsyncOperationStatus.id))
    author_profile_id = Column(Integer, ForeignKey(AuthorAccount.id))

    status = relationship("AsyncOperationStatus", foreign_keys=async_operation_status_id)
    author_profile = relationship("AuthorAccount", foreign_keys=author_profile_id)

    def __repr__(self):
        pass

# todo add events
# event.listen(
#     AsyncOperationStatus.__table__, "after_create",
#     DDL(""" INSERT INTO async_operation_status (id,code) VALUES(1,'pending'),(2, 'ok'),(3, 'error'); """)
# )
