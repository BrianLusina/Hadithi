from flask import render_template, Flask
from config import config


def create_app(config_name):
    """
    Defines a new application WSGI
    :param config_name:
    :return: the WSGI Flask object
    """
    app = Flask(__name__, template_folder='templates', static_folder="static")

    # configurations
    app.config.from_object(config[config_name])

    config[config_name].init_app(app)

    # initialize the db
    db.init_app(app)

    error_handlers(app)
    register_blueprints(app)
    return app


def error_handlers(app):
    """
    Error handlers for the app
    :param app: The app object
    """
    # Error handler for page not found
    @app.errorhandler(404)
    def not_found(error):
        return render_template('404.html')

    @app.errorhandler(403)
    def error_403(error):
        return render_template("403.html")

    @app.errorhandler(403)
    def error_500(error):
        return render_template("500.html")

    @app.errorhandler(400)
    def not_found(error):
        return render_template('400.html')


def register_blueprints(app):
    # Register blueprint(s) ALL blueprints will be registered here
    app.register_blueprint(home_module)
    app.register_blueprint(story_module)