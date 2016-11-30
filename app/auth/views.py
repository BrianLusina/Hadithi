from flask import Blueprint, render_template, request
from app.forms import LoginForm, RegisterForm

auth = Blueprint(name='auth', url_prefix='/auth', import_name=__name__)


@auth.route('/login', methods=["GET", "POST"])
def login():
    form = LoginForm(request.form)
    return render_template('auth/login.html', form=form)


@auth.route('/register', methods=["GET", "POST"])
def register():
    register_form = RegisterForm(request.form)
    return render_template('auth/register.html', register_form=register_form)