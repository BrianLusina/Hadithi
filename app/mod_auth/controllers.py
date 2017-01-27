from app import db
from app.mod_auth.facebook_auth import FacebookSignIn
from app.models import Author, AuthorAccount, FacebookAccount


def external_auth():
    """
    Will create an instance of FacebookSignIn class that will invoke a callback() method
    That will exchange code for an access token that will receive the user's data

    If we have the retrieved value of the facebook_id in our database, we’ll get the user object
    from a database.
    If the value isn’t in our database, we store it in the database, along with other data.
    At this point, the status of the async_operation will change to ok
    """
    oauth = FacebookSignIn()
    facebook_id, email, first_name, last_name = oauth.callback()