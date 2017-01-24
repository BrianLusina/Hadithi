"""
The email confirmation should contain a unique URL that a user simply needs to click in order to confirm his/her account.
Ideally, the URL should look something like this – http://hadithi.heroku.com/confirm/<id>.
The key here is the id. We are going to encode the user email (along with a timestamp) in the id using the
 itsdangerous package.
"""
from flask import current_app
from itsdangerous import URLSafeSerializer


def generate_confirmation_token(email):
    """
    Generates a confirmation token for the user to confirm their account
    The actual email is encoded in the token
    :param email: The user email
    :return:
    """
    serializer = URLSafeSerializer(current_app.config.get("SECRET_KEY"))
    return serializer.dumps(email, salt=current_app.config.get("SECURITY_PASSWORD_SALT"))


def confirm_token(token, expiration=3600):
    """
    we use the loads() method, which takes the token and expiration period
    :param token:
    :param expiration: validity of this token, set to 1hr
    :return: An email as long as the token has not expired
    """
    serializer = URLSafeSerializer(current_app.config.get("SECRET_KEY"))
    try:
        email = serializer.loads(
            token,
            salt=current_app.config.get("SECURITY_PASSWORD_SALT"),
            max_age=expiration
        )
        return email
    except:
        return False
