from flask import flash, session, redirect, url_for
from app import db
from .models import AuthorAccount, FacebookAccount, TwitterAccount, AsyncOperationStatus, AsyncOperation
from datetime import datetime
from .oauth import OAuthSignIn


def external_auth(provider_name):
    """
    Will create an instance of FacebookSignIn class that will invoke a callback() method
    That will exchange code for an access token that will receive the user's data

    If we have the retrieved value of the facebook_id in our database, we’ll get the user object
    from a database.
    If the value isn’t in our database, we store it in the database, along with other data.
    At this point, the status of the async_operation will change to ok
    """
    oauth = OAuthSignIn.get_provider(provider_name)
    provider_id, email, first_name, last_name = oauth.callback()

    if provider_id is None:
        flash(message="Authentication failed", category="error")

        # change the status for async operation to error
        status_error = AsyncOperationStatus.query.filter_by(code="error").first()

        async_operation = AsyncOperation.query.filter_by(id=session["async_operation_id"]).first()

        print("AsyncOperation ID", async_operation.id)

        async_operation.async_operation_status_id = status_error.id
        db.session.add(async_operation)
        db.session.commit()

        return redirect(url_for("auth.error"))

    # check provider being used in order to determine which dictionary to query
    if provider_name == "facebook":
        authenticate_with_facebook(provider_id, email, first_name, last_name)
    if provider_name == "twitter":
        authenticate_with_twitter(provider_id)


def authenticate_with_facebook(provider_id, *args):
    """
    authenticates with facebook
    :return:
    """
    # retrieve the user data from db for their facebook account
    author_facebook = FacebookAccount.query.filter_by(facebook_id=provider_id).first()
    email, first_name, last_name = args

    # if the author is new, we store their credentials in the database
    if not author_facebook:
        # first add the author account
        # the password will be auto-generated, this is because the user is logging in with their
        # external service account and not with their email and password
        # TODO: auto-generate password
        author_account = AuthorAccount(first_name=first_name, last_name=last_name, email=email,
                                       username=email, confirmed=True,
                                       registered_on=datetime.now(), password="")
        db.session.add(author_account)
        db.session.commit()

        # then create their facebook account which we can then update the author account id
        author_facebook = FacebookAccount(provider_id, email, first_name, last_name)
        author_facebook.author_id = author_account.id

        # add to session and commit to db
        db.session.add(author_facebook)
        db.session.commit()

        update_async_operation_status(author_facebook.id)


def authenticate_with_twitter(provider_id, *args):
    """
    Authenticates a user with Twitter and stores data in db
    :param provider_id: provider id from auth flow
    :param args variable number of arguments
    :return:
    """
    # retrieve the user data from db for their facebook account
    author_twitter = TwitterAccount.query.filter_by(twitter_id=provider_id).first()
    email, first_name, last_name = args

    # if the author is new, we store their credentials in the database
    if not author_twitter:
        # first add the author account
        # the password will be auto-generated, this is because the user is logging in with their
        # external service account and not with their email and password
        # TODO: auto-generate password
        author_account = AuthorAccount(first_name=first_name, last_name=last_name, email=email,
                                       username=email, confirmed=True,
                                       registered_on=datetime.now(), password="")
        db.session.add(author_account)
        db.session.commit()

        # then create their facebook account which we can then update the author account id
        author_twitter = TwitterAccount(provider_id, email, first_name, last_name)
        author_twitter.author_id = author_account.id

        # add to session and commit to db
        db.session.add(author_twitter)
        db.session.commit()

        update_async_operation_status(author_twitter.id)


def update_async_operation_status(author_provider_id):
    """
    updates async operation status
    :return:
    """
    status_ok = AsyncOperationStatus.query.filter_by(code="ok").first()
    async_operation = AsyncOperation.query.filter_by(id=session["async_operation_id"]).first()
    async_operation.async_operation_status_id = status_ok.id
    async_operation.user_profile_id = author_provider_id
    db.session.add(async_operation)
    db.session.commit()
