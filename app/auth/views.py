from flask import Blueprint, render_template, request, flash, redirect, url_for
from app.forms import LoginForm, RegisterForm
from app.models import Author
from app import db


auth = Blueprint(name='auth', url_prefix='/auth', import_name=__name__)


@auth.route('/login', methods=["GET", "POST"])
def login():
    login_form = LoginForm(request.form)
    return render_template('auth/login.html', login_form=login_form)


@auth.route('/register', methods=["GET", "POST"])
def register():
    register_form = RegisterForm(request.form)
    if request.method == "POST":
        if register_form.validate_on_submit():
            author = Author(fname=register_form.first_name.data, lname=register_form.second_name.data,
                            email=register_form.email.data, password=register_form.password.data)
            db.session.add(author)
            db.session.commit()
            flash("Thank you for registering")
            return redirect(url_for('auth.login'))
    return render_template('auth/register.html', register_form=register_form)
