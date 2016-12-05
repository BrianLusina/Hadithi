from flask import Blueprint, render_template, redirect, url_for
from flask_login import current_user, login_required
from app.models import Author, Story
dashboard = Blueprint(name="dashboard", url_prefix="/dashboard", import_name=__name__)


@dashboard.route("/<string:username>")
@login_required
def user_dashboard(username):
    """
    Displays all stories/articles written by this author in a grid
    :return user dashboard
    """
    user = current_user
    author = Author.filter_by(id=user.id)
    stories = Story.query.filter_by(author_id=author.id)
    return render_template("dashboard/userdashboard.html", user=user, stories=stories)
