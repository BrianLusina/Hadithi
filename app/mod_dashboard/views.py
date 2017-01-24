from flask import Blueprint, render_template, redirect, url_for, request, flash
from flask_login import current_user, login_required
from app.models import Author, Story
from app.forms import StoryForm
from app.utils.decorators import check_confirmed
from app import db
from app.mod_auth.token import generate_confirmation_token
from app.mod_auth.email import send_mail

dashboard = Blueprint(name="dashboard", url_prefix="/dashboard", import_name=__name__)


@dashboard.route('/unconfirmed')
@login_required
def unconfirmed():
    """
    Unconfirmed route for users who have not confirmed their email accounts.
    :return: template for unconfirmed users
    """
    # if the user is confirmed, take them to their dashboard
    if current_user.confirmed:
        return redirect(url_for('dashboard.user_dashboard', username=current_user.full_name))
    flash(message='Please confirm your account!', category='warning')
    return render_template('auth/unconfirmed.html', user=current_user)


@dashboard.route('/resend')
@login_required
def resend_confirmation():
    """
    Resend confirmation view
    This re-sends a confirmation email for the user to confirm their account before proceeding to
    their dashboard
    :return: a redirect to the unconfirmed route
    """
    # generate a new token to be sent
    token = generate_confirmation_token(current_user.email)

    # create a confirm url
    confirm_url = url_for('auth.confirm_email', token=token, _external=True)

    # build a message
    html = render_template('auth/activate.html', confirm_url=confirm_url, user=current_user)
    subject = "Please confirm your email"

    # send the email
    send_mail(current_user.email, subject, html)

    flash(message='A new confirmation email has been sent.', category='success')

    # redirect back to the unconfirmed route
    return redirect(url_for('dashboard.unconfirmed'))


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
@login_required
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
            return redirect(url_for('dashboard.user_dashboard', username=user.full_name))
    return render_template("dashboard/new_story.html", user=user, story_form=story_form)
