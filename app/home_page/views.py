from app.home_page import home_module
from flask import render_template


@home_module.route('/')
@home_module.route('index')
@home_module.route('home')
def home():
    return render_template('home/index.html')
