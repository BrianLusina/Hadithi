"""
The email confirmation should contain a unique URL that a user simply needs to click in order to confirm his/her account.
Ideally, the URL should look something like this – http://hadithi.heroku.com/confirm/<id>.
The key here is the id. We are going to encode the user email (along with a timestamp) in the id using the
 itsdangerous package.
"""

from itsdangerous import URLSafeSerializer
from app import create_app
import os

# create app instance base on the current environment, or default it
app = create_app(os.getenv('FLASK_CONFIG') or 'default')


def generate_confirmation_token(email):
    """
    Generates a confirmation token for the user to confirm their account
    The actual email is encoded in the token
    :param email: The user email
    :return:
    """
    serializer = URLSafeSerializer(app.config["SECRET_KEY"])
    return serializer.dumps(email, salt=app.config["SECURITY_PASSWORD_SALT"])


def confirm_token(token, expiration=3600):
    """
    we use the loads() method, which takes the token and expiration period
    :param token:
    :param expiration: validity of this token, set to 1hr
    :return: An email as long as the token has not expired
    """
    serializer = URLSafeSerializer(app.config["SECRET_KEY"])
    try:
        email = serializer.loads(
            token,
            salt = app.config["SECURITY_PASSWORD_SALT"],
            max_age=expiration
        )
    except:
        return False
    return email
