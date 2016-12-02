from flask import Blueprint, render_template, request, flash, redirect, url_for
from sqlalchemy.exc import IntegrityError
from app.forms import LoginForm, RegisterForm, ForgotPassword
from app.models import Author
from app import db

auth = Blueprint(name='auth', url_prefix='/auth', import_name=__name__)


@auth.route('/login', methods=["POST", "GET"])
def login():
    """
    Login route for user's to login to their accounts
    :return: Login view
    """
    login_form = LoginForm(request.form, prefix="login-form")

    if request.method == "POST" and request.form["login"] == "LOGIN":
        if login_form.validate_on_submit():
            author = Author.query.filter_by(email=login_form.email.data).first()
            if author is not None and author.verify_password(login_form.password.data):
                # todo: redirect to author dashboard
                return redirect(url_for('home.home'))
            else:
                # todo: display error
                return render_template('auth/auth.html')
    return render_template('auth/auth.html', login_form=login_form, register_form=RegisterForm())


@auth.route('/login', methods=["POST", "GET"])
def register():
    """
    Processes the registration form details. This is used to add the user to the database, if they
    are not there, redirects them to their dashboard when registration is complete
    :return the register form
    """
    register_form = RegisterForm(request.form, prefix="register-form")
    if request.method == "POST":
        if request.form["register"] == "REGISTER" and register_form.validate_on_submit():
            author = Author(full_name=register_form.full_name.data, email=register_form.email.data,
                            password=register_form.password.data)
            print(author)
            try:
                db.session.add(author)
                db.session.commit()
            except IntegrityError as ie:
                # todo: display error
                print(ie)
                db.session.rollback()
            return redirect(url_for('home.home'))
    return render_template('auth/auth.html', register_form=register_form, login_form=LoginForm())


@auth.route('/forgot-password', methods=["GET", "POST"])
def forgot_password():
    forgot_pass = ForgotPassword(request.form)
    return render_template('auth/password-recovery.html', forgot_pass=forgot_pass)
