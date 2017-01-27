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
            state=current_app.config["CSRF_SESSION_KEY "],
            redirect_uri=self.get_callback_url()
        ))

    