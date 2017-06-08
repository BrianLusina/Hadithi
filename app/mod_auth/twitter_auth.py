"""
Twitter authentication file. used to sign in a user with Twitter

Specifies rules to use
"""
from flask import current_app, redirect, url_for, request
from rauth import OAuth2Service


class TwitterSignIn(object):
    """
    Twitter sign in class responsible for signing in with Twitter
    """

    def __init__(self):
        """
        Creates an instance of TwitterSignIn class
        :return: TwitterSignIn object
        :rtype: TwitterSignIn
        """
        credentials = current_app.config["OAUTH_CREDENTIALS"]["twitter"]
        self.consumer_key = credentials["consumer_key"]
        self.consumer_secret = credentials["consumer_secret"]

        self.service = OAuth2Service(
            name="twitter",
            client_id=self.consumer_key,
            client_secret=self.consumer_secret,
            authorize_url='https://api.twitter.com/oauth/authenticate',
            access_token_url='https://api.twitter.com/oauth/access_token',
            base_url='https://api.twitter.com/1/',
        )

    @staticmethod
    def get_callback_url():
        """
        The redirect uri that will kick off background processes with Facebook
        :return: A redirect for the pre-loader to start background communication with facebook
        """
        return url_for("auth.show_preloader_start_auth", _external=True)

    def authorize(self):
        """
        Redirects the user to Facebook login page, where they are prompted to accept permissions
        scope:
            Will request for specific user permissions, such as public profile and email,
            public_profile will contain facebook id, first and last names
            email: will be the user's email signed in with facebook
        redirect_uri:
            the url we will redirect the user to
        state: A unique string created by our app to protect against cross-site request forgery.
        client_id: This value is automatically added to the requested parameters by the Rauth’s
         get_authorize_url() method.
         used to protect our app from accepting a code intended for an application with a different client_id.
        :return: a redirect to Facebook login page
        """
        return redirect(self.service.get_authorize_url(
            scope="public_profile,email",
            response_type="code",
            state=current_app.config["CSRF_SESSION_KEY"],
            redirect_uri=self.get_callback_url()
        ))

    def callback(self):
        """
        Checks if the code is in the response and returns the user's, facebook_id, email,
         first_name, last_name in that order
        if code is not in the request args, it will return a 4 element tuple of None
        If the url has a code, we ask for a token using get_auth_session
        :return: User scope as a tuple
        :rtype: tuple
        """
        if "code" not in request.args:
            return None, None, None, None
        oauth_session = self.service.get_auth_session(
            date={"code": request.args["code"],
                  "grant_type": "authorization_code",
                  "redirect_uri": self.get_callback_url()
                  }
        )
        user_twitter_data = oauth_session.get("me?fields=id,email,first_name,last_name").json()
        return (
            user_twitter_data["id"],
            user_twitter_data.get("email"),
            user_twitter_data.get("first_name"),
            user_twitter_data.get("last_name")
        )
