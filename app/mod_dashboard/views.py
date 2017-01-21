from flask import Blueprint, render_template, redirect, url_for, request, flash
from flask_login import current_user, login_required
from app.models import Author, Story
from app.forms import StoryForm
from app.utils.decorators import check_confirmed
from app import db
from app.mod_auth.token import generate_confirmation_token
from app.mod_auth.email import send_mail


dashboard = Blueprint(name="dashboard", url_prefix="/dashboard", import_name=__name__)


@dashboard.route("/<string:username>")
@login_required
@check_confirmed
def user_dashboard(username):
    """
    Displays all stories/articles written by this author in a grid
    Cheks if the user is logged in and logs them into their dashboard,
    Checks if the user has been confirmed and display the dashboard if they have
    :return user dashboard
    """
    user = current_user
    stories = Story.query.filter_by(author_id=user.id).all()
    return render_template("dashboard/userdashboard.html", user=user, stories=stories)


@dashboard.route("/new-story", methods=["POST", "GET"])
def write_story():
    """
    Allows Author to write a new story
    :return new story template
    """
    story_form = StoryForm(request.form)
    user = current_user
    if request.method == "POST":
        if story_form.validate_on_submit():
            story = Story(title=story_form.story_title.data, tagline=story_form.tagline.data,
                          category=story_form.category.data, content=story_form.content.data,
                          author_id=user.id)
            db.session.add(story)
            db.session.commit()
            return redirect(url_for('dashboard.user_dashboard', user.full_name))
    return render_template("dashboard/new_story.html", user=user, story_form=story_form)


@dashboard.route('/resend')
@login_required
def resend_confirmation():
    token = generate_confirmation_token(current_user.email)
    confirm_url = url_for('auth.confirm_email', token=token, _external=True)
    html = render_template('auth/activate.html', confirm_url=confirm_url, user=current_user)
    subject = "Please confirm your email"
    send_mail(current_user.email, subject, html)
    flash('A new confirmation email has been sent.', 'success')
    return redirect(url_for('auth.unconfirmed'))
