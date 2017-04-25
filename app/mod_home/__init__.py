from flask import Blueprint

home_module = Blueprint(name='home', url_prefix='/', import_name=__name__,
                        template_folder="templates")

from . import views
