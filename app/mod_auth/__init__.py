from flask import Blueprint

auth = Blueprint(name='auth', url_prefix='/auth', import_name=__name__)

from . import views

