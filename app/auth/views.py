from flask import Blueprint, render_template, request, flash, redirect, url_for
from sqlalchemy.exc import IntegrityError
from app.forms import LoginForm, RegisterForm, ForgotPassword
from app.models import Author
from app import db
from flask_login import logout_user, login_required, login_user, current_user


auth = Blueprint(name='auth', url_prefix='/auth', import_name=__name__)


@auth.route('/login', methods=["POST", "GET"])
def login():
    """
    Login route for user's to login to their accounts
    :return: Login view
    """
    login_form = LoginForm(request.form, prefix="login-form")

    if request.method == "POST":
        if login_form.validate_on_submit():
            author = Author.query.filter_by(email=login_form.email.data).first()
            if author is not None and author.password_hash == login_form.password.data:
                # todo: redirect to author dashboard
                login_user(author, login_form.remember_me.data)
                return redirect(url_for('home.home'))
            flash("Invalid username or password", "error")
    return render_template('auth/login.html', login_form=login_form)


@auth.route('/register', methods=["POST", "GET"])
def register():
    """
    Processes the registration form details. This is used to add the user to the database, if they
    are not there, redirects them to their dashboard when registration is complete
    :return the register form
    """
    register_form = RegisterForm(request.form, prefix="register-form")
    if request.method == "POST":
        if register_form.validate_on_submit():
            author = Author(full_name=register_form.full_name.data, email=register_form.email.data,
                            password=register_form.password.data)
            try:
                db.session.add(author)
                db.session.commit()
            except IntegrityError as ie:
                # todo: display error
                print(ie)
                db.session.rollback()
            return redirect(url_for('auth.login'))
    return render_template('auth/register.html', register_form=register_form)


@auth.route('/forgot-password', methods=["GET", "POST"])
def forgot_password():
    forgot_pass = ForgotPassword(request.form)
    return render_template('auth/password-recovery.html', forgot_pass=forgot_pass)


@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for("home.home"))

