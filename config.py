import os

basedir = os.path.abspath(os.path.dirname(__file__))
APP_ROOT = os.path.dirname(os.path.abspath(__file__))


class Config(object):
    """
    Global configuration from which other configs inherit
    :cvar THREADS_PER_PAGE: Application threads. A common general assumption is
    using 2 per available processor cores - to handle
    incoming requests using one and performing background
    operations using the other.
    :cvar CSRF_SESSION_KEY Use a secure, unique and absolutely secret key for signing the data.
    :cvar SQLALCHEMY_DATABASE_URI Define the database - we are working with SQLite for this example
    """
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'hadithi'
    SQLALCHEMY_COMMIT_ON_TEARDOWN = True
    SQLALCHEMY_MIGRATE_REPO = os.path.join(basedir, 'db_repository')
    SQLALCHEMY_TRACK_MODIFICATIONS = True
    SQLALCHEMY_DATABASE_URI = os.environ.get("DATABASE_URL")
    SECURITY_PASSWORD_SALT = os.environ.get("SECURITY_PASSWORD_SALT") or 'my_precious_two'
    ROOT_DIR = APP_ROOT
    WTF_CSRF_ENABLED = True
    CSRF_ENABLED = True
    CSRF_SESSION_KEY = os.environ.get("CSRF_SESSION_KEY")
    THREADS_PER_PAGE = 2
    DATABASE_CONNECT_OPTIONS = {}

    # mail settings
    MAIL_SERVER = 'smtp.googlemail.com'
    MAIL_PORT = 465
    MAIL_USE_TLS = False
    MAIL_USE_SSL = True

    # gmail authentication
    MAIL_USERNAME = os.environ.get('APP_MAIL_USERNAME')
    MAIL_PASSWORD = os.environ.get('APP_MAIL_PASSWORD')

    MAIL_DEFAULT_SENDER = os.environ.get("MAIL_DEFAULT_SENDER")

    # credentials for external service accounts
    OAUTH_CREDENTIALS = dict(facebook=dict(id=os.environ.get("FACEBOOK_ID"),
                                           secret=os.environ.get("FACEBOOK_SECRET")),
                             google=dict(id=os.environ.get("GOOGLE_ID"),
                                         secret=os.environ.get("GOOGLE_SECRET")),
                             twitter=dict(id=os.environ.get("TWITTER_KEY"),
                                          secret=os.environ.get("TWITTER_SECRET"))
                             )

    @staticmethod
    def init_app(app):
        pass


class DevelopmentConfig(Config):
    """
    Development configuration
    """
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL')
    # SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'app.db')


class TestingConfig(Config):
    """
    Testing configurations
    """
    DEBUG = True
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'
    WTF_CSRF_ENABLED = False
    CSRF_ENABLED = False
    PRESERVE_CONTEXT_ON_EXCEPTION = False


class ProductionConfig(Config):
    """
    Production configuration
    """
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL')
    ADMINS = [os.environ.get("ADMIN_EMAIL_1")]

config = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig
}
