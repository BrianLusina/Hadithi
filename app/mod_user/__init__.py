from flask import Blueprint

author = Blueprint(name="author", url_prefix="/author", import_name=__name__)

from . import views
