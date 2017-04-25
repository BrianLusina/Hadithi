from flask import Blueprint

story_module = Blueprint(name='story', url_prefix='/story', import_name=__name__,
                         template_folder="templates")

from . import views
