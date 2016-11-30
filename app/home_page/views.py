from flask import render_template, Blueprint
home_module = Blueprint(name='home', url_prefix='/', import_name=__name__)


@home_module.route('/')
@home_module.route('index')
@home_module.route('home')
def home():
    return render_template('home/index.html')


@home_module.route('contact')
def contact():
    return render_template('home/contact.html')


@home_module.route('about')
def about():
    return render_template('home/about.html')


