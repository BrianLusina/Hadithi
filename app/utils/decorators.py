from functools import wraps
from flask import flash, redirect, url_for
from flask_login import current_user


def check_confirmed(func):
    """
    Function to check whether a user has been confirmed. If unconfirmed, will redirect to
    unconfirmed view
    :param func: function to be decorated
    :return: decorated function
    """

    @wraps(func)
    def decorated_function(*args, **kwargs):
        if current_user.confirmed is False:
            flash(message="Please confirm your account", category="warning")
            return redirect(url_for('dashboard.unconfirmed'))
        return func(*args, **kwargs)

    return decorated_function
