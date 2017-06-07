"""
module that will handle following and unfollowing of authors
"""

from . import author
from flask import redirect, url_for, flash
from app.mod_auth.models import AuthorAccount
from app import db
from flask_login import current_user, login_required


@author.route("/follow/<username>")
@login_required
def follow(username):
    """
    Follow route to enable current user to follow this specified user
    :param username: username of the intended followee
    :return: a redirect to home page
    """
    author = AuthorAccount.query.filter_by(username=username).first()

    # current user can not follow someone who is not there
    if author is None:
        flash(message="Author %s not found" % username, category="error")
        return redirect(url_for("home.home"))

    # current user can not follow themselves
    if author == current_user:
        flash(message="You can't follow yourself!", category="error")
        return redirect(url_for("dashboard", username=current_user.username))

    u = current_user.follow(author)

    if u is None:
        flash(message="Can't follow %s" % username, category="error")
        return redirect(url_for("home.home"))

    db.session.add(u)
    db.session.commit()
    flash(message="You are now following %s" % username, category="success")
    return redirect(url_for("home.home"))


@author.route("/unfollow/<username>")
@login_required
def unfollow(username):
    """
    Unfollow user to enable current user to unfollow a specified user with username
    :param username: the username to unfollow
    :return: a redirect to home page
    """
    author = AuthorAccount.query.filter_by(username=username).first()

    if author is None:
        flash(message="Author %s not found" % username, category="error")
        return redirect(url_for("home.home"))

    if author == current_user:
        flash(message="You can't unfollow yourself!", category="error")
        return redirect(url_for("home.home"))

    u = current_user.unfollow(author)

    if u is None:
        flash(message="Cannot unfollow %s" % username, category="error")
        return redirect(url_for("home.home"))

    db.session.add(u)
    db.session.commit()
    flash(message="You are no longer following %s" % username, category="success")
    return redirect(url_for("home.home"))


