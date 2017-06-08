"""
Twitter authentication file. used to sign in a user with Twitter

Specifies rules to use
"""
from flask import current_app, request, session, redirect
from rauth import OAuth1Service
from .oauth import OAuthSignIn


class TwitterSignIn(OAuthSignIn):
    """
    Twitter sign in class responsible for signing in with Twitter
    """

    def __init__(self, provider_name):
        """
        Creates an instance of TwitterSignIn class
        :return: TwitterSignIn object
        :rtype: TwitterSignIn
        """
        super(TwitterSignIn, self).__init__("twitter")

        self.service = OAuth1Service(
            name="twitter",
            consumer_key=self.consumer_id,
            consumer_secret=self.consumer_secret,
            request_token_url="https://api.twitter.com/oauth/request_token",
            authorize_url='https://api.twitter.com/oauth/authenticate',
            access_token_url='https://api.twitter.com/oauth/access_token',
            base_url='https://api.twitter.com/1/',
        )

    def authorize(self):
        """
        obtaining a request token from the provider, which is a list of two items,
        the first of which is then used as an argument in the redirect.
        The entire request token is saved to the user session because it will be needed again in
         the callback.
        :return: redirect object
        """
        request_token = self.service.get_request_token(
            params={"oauth_callback": self.get_callback_url()})
        session["request_token"] = request_token
        return redirect(self.service.get_authorize_url(request_token[0]))

    def callback(self):
        request_token = session.pop("request_token")

        if "oauth_verifiere" not in request.args:
            return None, None, None, None

        oauth_session = self.service.get_auth_session(
            request_token[0], request_token[1],
            data={"oauth_verifier": request.args["oauth_verifier"],}
        )
        twitter_session = oauth_session.get("account/verify_credentials.json").json()
        twitter_id = "twitter$" + str(twitter_session.get("id"))
        username = twitter_session.get("screen_name")

        return twitter_id, username, None

