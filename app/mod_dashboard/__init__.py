from flask import Blueprint

dashboard = Blueprint(name="dashboard", url_prefix="/dashboard", import_name=__name__)

from . import views
