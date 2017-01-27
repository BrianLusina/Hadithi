from flask import current_app, redirect, url_for, request, session
from rauth import OAuth2Service


class FacebookSignIn(object):
    """
    Class to handle authentication with facebook
    """
    def __init__(self):
        """
        Initializes a new facebook auth object to handle authentication with Facebook
        Because Facebook uses OAuth2 service, we initialize a with OAuth2Service
        """
        # get the credentials for facebook
        credentials = current_app.config["OAUTH_CREDENTIALS"]["facebook"]
        self.consumer_id = credentials["id"]
        self.consumer_secret = credentials["secret"]

        # initialize a new auth2 service with app credentials and urls
        # authorize_url: URL used to connect during user facebook auth
        # access_token_url: URL for which a request is made to exchange a code for an access token
        # base_url: URL, prefix for making Facebook API requests
        self.service = OAuth2Service(
            name="facebook",
            client_id=self.consumer_id,
            client_secret=self.consumer_secret,
            authorize_url='https://www.facebook.com/dialog/oauth',
            access_token_url='https://graph.facebook.com/oauth/access_token',
            base_url='https://graph.facebook.com/'
        )
    