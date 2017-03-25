from flask import render_template, Flask
from config import config
from flask_login import LoginManager, current_user
from flask_sqlalchemy import SQLAlchemy
from flask_mail import Mail
from datetime import datetime

db = SQLAlchemy()
login_manager = LoginManager()
login_manager.session_protection = 'strong'
login_manager.login_view = 'auth.login'
mail = Mail()


def create_app(config_name):
    """
    Defines a new application WSGI. Creates the flask application object that will be used to define and
    create the whole application
    :param config_name: the configuration to use when creating a new application
    :return: the newly created and configured WSGI Flask object
    :rtype: Flask
    """
    app = Flask(__name__, template_folder='templates', static_folder="static")

    # configurations
    app.config.from_object(config[config_name])
    config[config_name].init_app(app)

    # initialize the db and login manager, flask mail
    db.init_app(app)
    login_manager.init_app(app)
    mail.init_app(app)

    error_handlers(app)
    request_handlers(app, db)
    register_blueprints(app)
    set_logger(app, config_name)

    return app


def error_handlers(app):
    """
    Error handlers for the app
    :param app: The app object
    """

    # Error handler for page not found
    @app.errorhandler(404)
    def not_found(error):
        return render_template('errorpages/404.html', user=current_user)

    @app.errorhandler(403)
    def error_403(error):
        return render_template("errorpages/403.html", user=current_user)

    @app.errorhandler(403)
    def error_500(error):
        return render_template("errorpages/500.html", user=current_user)

    @app.errorhandler(400)
    def not_found(error):
        return render_template('errorpages/400.html', user=current_user)


def request_handlers(app, db_):
    """
    Handles requests sent by the application
    :param app: the current application
    :param db_: current database
    :return:
    """

    @app.before_request
    def before_request():
        """
        Before submitting the request, change the currently logged in user 'last seen' status to now
        this will update the database last_seen column and every time the user makes a request (refreshes the
        page), the last seen will be updated. this is called before any request is ma
        """
        if current_user.is_authenticated:
            current_user.last_seen = datetime.now()
            db_.session.add(current_user)
            db_.session.commit()

    # @app.after_request
    # def after_request(response):
    #     for query in get_debug_queries():
    #         if query.duration >= DATABASE_QUERY_TIMEOUT:
    #             app.logger.warning(
    #                 "SLOW QUERY: %s\nParameters: %s\nDuration: %fs\nContext: %s\n" %
    #                 (query.statement, query.parameters, query.duration,
    #                  query.context))
    #     return response


def set_logger(app, config_name):
    """
    Sets logging of error messages in case they occur in the application. This will send an email to
    any of the administrators, or all of the administrators.
    This should work when the application is in production
    :param app: current Flask app
    :param config_name: the configuration to use this, normally in Production
    """
    if config_name == "production":
        MAIL_SERVER = app.config.get("MAIL_SERVER")
        if not app.debug and MAIL_SERVER != "":
            import logging
            from logging.handlers import SMTPHandler
            credentials = None

            MAIL_USERNAME = app.config.get("MAIL_USERNAME")
            MAIL_PASSWORD = app.config.get("MAIL_PASSWORD")

            if MAIL_USERNAME or MAIL_PASSWORD:
                credentials = (MAIL_USERNAME, MAIL_PASSWORD)

            mail_handler = SMTPHandler(mailhost=(MAIL_SERVER, app.config.get("MAIL_HOST")),
                                       fromaddr="no-reply@" + MAIL_SERVER,
                                       toaddrs=app.config.get("ADMINS"),
                                       subject="Hadithi app failure",
                                       credentials=credentials)
            mail_handler.setLevel(logging.ERROR)
            app.logger.addHandler(mail_handler)

def register_blueprints(app):
    """
    Registers tall blueprints in the app
    :param app: The current flask application
    """
    from app.mod_home import home_module
    from app.mod_story.views import story_module
    from app.mod_auth import auth
    from app.mod_dashboard import dashboard

    app.register_blueprint(home_module)
    app.register_blueprint(story_module)
    app.register_blueprint(auth)
    app.register_blueprint(dashboard)
