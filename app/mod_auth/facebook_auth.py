from flask import current_app, redirect, url_for, request
from rauth import OAuth2Service
from .oauth import OAuthSignIn


class FacebookSignIn(OAuthSignIn):
    """
    Class to handle authentication with facebook
    """

    def __init__(self, provider_name):
        """
        Initializes a new facebook auth object to handle authentication with Facebook
        Because Facebook uses OAuth2 service, we initialize a with OAuth2Service
        """
        # get the credentials for facebook
        super(FacebookSignIn, self).__init__("facebook")

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
        return redirect(self.service.get_authorize_url(
            scope="public_profile,email",
            response_type="code",
            state=current_app.config["CSRF_SESSION_KEY"],
            redirect_uri=self.get_callback_url()
        ))

    @staticmethod
    def get_callback_url():
        return url_for("auth.show_preloader_start_auth", _external=True)

    def callback(self):
        if "code" not in request.args:
            return None, None, None, None
        oauth_session = self.service.get_auth_session(
            date={"code": request.args["code"],
                  "grant_type": "authorization_code",
                  "redirect_uri": self.get_callback_url()
                  }
        )
        user_facebook_data = oauth_session.get("me?fields=id,email,first_name,last_name").json()
        return (
            user_facebook_data["id"],
            user_facebook_data.get("email"),
            user_facebook_data.get("first_name"),
            user_facebook_data.get("last_name")
        )
