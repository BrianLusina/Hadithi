from flask import Blueprint, render_template, request, flash, redirect, url_for
from app.forms import LoginForm, RegisterForm
from app.models import Author
from app import db


auth = Blueprint(name='auth', url_prefix='/auth', import_name=__name__)


@auth.route('/login', methods=["GET", "POST"])
def login():
    """
    Login route for user's to login to their accounts
    :return: Login view
    """
    login_form = LoginForm(request.form)
    register_form = RegisterForm(request.form)

    if request.method == "POST":
        if login_form.validate_on_submit():
            author = Author.query.filter_by(email=login_form.email.data).first()
            if author is not None and author.verify_password(login_form.password.data):
                # todo: redirect to author dashboard
                return redirect(url_for('home.home'))
            flash('Invalid username or password.', 'error')

        if register_form.validate_on_submit():
            author = Author(fname=register_form.full_name.data, email=register_form.email.data,
                            password=register_form.password.data)
            db.session.add(author)
            db.session.commit()
            flash("Thank you for registering")
            return redirect(url_for('auth.login'))
    return render_template('auth/auth.html', login_form=login_form, register_form=register_form)
