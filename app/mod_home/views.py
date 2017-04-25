from . import home_module
from flask import render_template, request
from flask_login import current_user
from app.models import Story, AuthorAccount
from app.forms import ContactForm


@home_module.route('/')
@home_module.route('index')
@home_module.route('home')
def index():
    # stories = Story.query.all()
    author = AuthorAccount
    context = dict(
        author=author,
        user=current_user
    )
    return render_template('home.index.html', **context)


@home_module.route('contact')
def contact():
    user = current_user
    contact_form = ContactForm(request.form)
    return render_template('home.contact.html', user=user, contact_form=contact_form)


@home_module.route('about')
def about():
    """
    About content, displays about page
    :return:
    """
    user = current_user
    return render_template('home.about.html', user=user)


@home_module.route("google-site-verification: google2f512247f9616fa3.html")
def google_verification():
    return render_template("google2f512247f9616fa3.html")
