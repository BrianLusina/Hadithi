from flask import Blueprint, render_template, request, flash, redirect, url_for
from app.forms import LoginForm, RegisterForm, ForgotPassword
from app.models import Author
from app import db


auth = Blueprint(name='auth', url_prefix='/auth', import_name=__name__)


@auth.route('/login', methods=["POST"])
def login():
    """
    Login route for user's to login to their accounts
    :return: Login view
    """
    login_form = LoginForm(request.form, prefix="login_form")

    if request.method == "POST" and login_form.login.data:
        if login_form.validate_on_submit():
            author = Author.query.filter_by(email=login_form.email.data).first()
            if author is not None and author.verify_password(login_form.password.data):
                # todo: redirect to author dashboard
                return redirect(url_for('home.home'))
    return render_template('auth/auth.html', login_form=login_form, register_form=RegisterForm())


@auth.route('/register', methods=["POST"])
def register():
    """
    Processes the registration form details. This is used to add the user to the database, if they
    are not there, redirects them to their dashboard when registration is complete
    :return the register form
    """
    register_form = RegisterForm(request.form, prefix="register_form")

    if request.method == "POST" and register_form.register.data:
        if register_form.validate_on_submit():
            author = Author(full_name=register_form.full_name.data, email=register_form.email.data,
                            password=register_form.password.data)
            db.session.add(author)
            db.session.commit()
            return redirect(url_for('home.home'))

    return render_template('auth/auth.html', register_form=register_form, login_form=LoginForm())


@auth.route('/forgot-password', methods=["GET", "POST"])
def forgot_password():
    forgot_pass = ForgotPassword(request.form)
    return render_template('auth/password-recovery.html', forgot_pass=forgot_pass)
