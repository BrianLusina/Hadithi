from flask import Blueprint

auth = Blueprint(name='auth', url_prefix='/auth', import_name=__name__,
                 template_folder="templates", static_folder="static")

from . import views

