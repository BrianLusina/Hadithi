from flask import Blueprint, render_template, redirect, url_for, request
from flask_login import current_user, login_required
from app.models import Author, Story
from app.forms import StoryForm


dashboard = Blueprint(name="dashboard", url_prefix="/dashboard", import_name=__name__)


@dashboard.route("/<string:username>")
@login_required
def user_dashboard(username):
    """
    Displays all stories/articles written by this author in a grid
    :return user dashboard
    """
    user = current_user
    stories = Story.query.filter_by(author_id=user.id).all()
    return render_template("dashboard/userdashboard.html", user=user, stories=stories)

@dashboard.route("/new-story")
def write_story():
    """
    Allows Author to write a new story
    :return new story template
    """
    story_form = StoryForm(request.form)
    return render_template("dashboard/new_story.html", user=current_user, story_form=story_form) 