from flask import flash, session, redirect, url_for
from app import db
from app.mod_auth.facebook_auth import FacebookSignIn
from app.models import AuthorAccount, FacebookAccount, AsyncOperationStatus, AsyncOperation


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

    if facebook_id is None:
        flash(message="Authentication failed", category="error")

        # change the status for async operation to error
        status_error = AsyncOperationStatus.query.filter_by(code="error").first()

        async_operation = AsyncOperation.query.filter_by(id=session["async_operation_id"]).first()

        print("AsyncOperation ID", async_operation.id)

        async_operation.async_operation_status_id = status_error.id
        db.session.add(async_operation)
        db.session.commit()

        return redirect(url_for("auth.error"))

    # retrieve the user data from db for their facebook account
    author_facebook = FacebookAccount.query.filter_by(facebook_id=facebook_id).first()

    # if the author is new, we store their credentials in the database
    if not author_facebook:
        author_facebook = FacebookAccount(facebook_id, email, first_name, last_name)
        db.session.add(author_facebook)
        db.session.commit()

    status_ok = AsyncOperationStatus.query.filter_by(code="ok").first()
    async_operation = AsyncOperation.query.filter_by(id=session["async_operation_id"]).first()
    async_operation.async_operation_status_id = status_ok.id
    async_operation.user_profile_id = author_facebook.id
    db.session.add(async_operation)
    db.session.commit()

