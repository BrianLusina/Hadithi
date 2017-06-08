"""
will contain base class for OAuth sign in using external service accounts
This is neccessary as OAuth providers are many and making this generic enables using any OAuth
protocol (either 1 or 2) easy to add and maintain
"""
from flask import current_app, url_for
from abc import abstractmethod


class OAuthSignIn(object):
    """
    base class defines the structure that the subclasses that implement each provider must
     follow.
     The constructor initializes the provider's name,
     and the application id and secret assigned by it, which are obtained from the configuration.
     :cvar providers this is used to keep track of providers in the object hierarchy
    """

    providers = None

    def __init__(self, provider_name):
        """
        Creates an oauth sign in object
        obtains credentials from config object of application for the given provider

        :param provider_name name to use to authenticate with OAuth protocol
        """
        self.provider_name = provider_name
        credentials = current_app.config["OAUTH_CREDENTIALS"][provider_name]
        self.consumer_id = credentials["id"]
        self.consumer_secret = credentials["secret"]

    @abstractmethod
    def authorize(self):
        """
        Redirects the user to provider login page, where they are prompted to accept permissions
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
        :return: a redirect to provider login page
        """
        pass

    @abstractmethod
    def callback(self):
        """
        Checks if the code is in the response and returns the user's, facebook_id, email,
         first_name, last_name in that order
        if code is not in the request args, it will return a 4 element tuple of None
        If the url has a code, we ask for a token using get_auth_session
        :return: User scope as a tuple
        :rtype: tuple
        """
        pass

    @staticmethod
    def get_callback_url():
        """
        The redirect uri that will kick off background processes with Facebook
        :return: A redirect for the pre-loader to start background communication with facebook
        """
        return url_for("auth.show_preloader_start_auth", _external=True)

    @classmethod
    def get_provider(cls, provider_name):
        """
        Gets a given provider from a given subclass
        :param provider_name: provider name to use
        :return: provider that will be used for authentication
        """
        if cls.providers is None:
            cls.providers = {}
            for provider_class in cls.__subclasses__():
                provider = provider_class
                cls.providers[provider.provider_name] = provider

        return cls.providers[provider_name]
