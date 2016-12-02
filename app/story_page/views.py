from flask import Blueprint, render_template

story_module = Blueprint(name='story', url_prefix='/story', import_name=__name__)


@story_module.route('')
def view_story():
    return render_template("")