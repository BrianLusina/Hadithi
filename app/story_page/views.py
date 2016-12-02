from flask import Blueprint, render_template
from app.models import Story

story_module = Blueprint(name='story', url_prefix='/story', import_name=__name__)


@story_module.route('/<int:story_id>')
def view_story(story_id):
    """
    Displays the story for viewing.
    Takes in a specific story id to be used to display the story to the user
    :return: The template for the viewing story/ story being read
    """
    return render_template("")
