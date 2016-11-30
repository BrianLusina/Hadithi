from flask import Blueprint, render_template

auth = Blueprint(name='auth', url_prefix='/auth', import_name=__name__)


@auth.route('')
def login():
    return render_template('auth/login.html')
