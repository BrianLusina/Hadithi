from flask import render_template, Blueprint, request
from flask_login import current_user
from app.models import Story, Author
from app.forms import ContactForm
from app import db
home_module = Blueprint(name='home', url_prefix='/', import_name=__name__)


@home_module.route('/')
@home_module.route('index')
@home_module.route('home')
def home():
    stories = Story.query.all()
    author = Author
    user = current_user
    return render_template('home/index.html', stories=stories, author=author, user=user)


@home_module.route('contact')
def contact():
    user = current_user
    contact_form = ContactForm(request.form)
    return render_template('home/contact.html', user=user, contact_form=contact_form)


@home_module.route('about')
def about():
    """
    About content, displays about page
    :return:
    """
    user = current_user
    return render_template('home/about.html', user=user)


