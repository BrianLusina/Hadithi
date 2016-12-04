from flask import render_template, Blueprint
from flask_login import current_user
from app.models import Story, Author
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
    return render_template('home/contact.html')


@home_module.route('about')
def about():
    return render_template('home/about.html')


