from flask import Blueprint

dashboard = Blueprint(name="dashboard", url_prefix="/dashboard", import_name=__name__,
                      template_folder="templates", static_folder="static")

from . import views
