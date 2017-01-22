from flask import Blueprint, render_template, request, flash, redirect, url_for, current_app
from app.forms import LoginForm, RegisterForm, ForgotPassword
from app.models import Author
from app import db
from flask_login import logout_user, login_required, login_user, current_user
from app.mod_auth.token import generate_confirmation_token, confirm_token
from datetime import datetime
from app.mod_auth.email import send_mail

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
            if author is not None and author.verify_password(login_form.password.data):
                login_user(author, login_form.remember_me.data)
                flash(message="Welcome back {}!".format(author.full_name), category="success")
                return redirect(url_for('dashboard.user_dashboard', username=author.full_name))
            flash("Invalid email and/or password", "error")
    return render_template('auth/login.html', login_form=login_form, user=current_user)


@auth.route('/register', methods=["POST", "GET"])
def register():
    """
    Processes the registration form details. This is used to add the user to the database, if they
    are not there, redirects them to their dashboard when registration is complete

    Sends and email verification to user based on the email provided.
    :return the register form
    """
    register_form = RegisterForm(request.form, prefix="register-form")
    if request.method == "POST":
        if register_form.validate_on_submit():
            author = Author(full_name=register_form.full_name.data, email=register_form.email.data,
                            password=register_form.password.data, confirmed=False,
                            registered_on=datetime.now())
            db.session.add(author)
            db.session.commit()

            # generate token for email verification
            token = generate_confirmation_token(author.email)

            # _external adds the full absolute URL that includes the hostname and port
            confirm_url = url_for('auth.confirm_email', token=token, _external=True)

            html = render_template('auth/confirm_email.html', confirm_url=confirm_url,
                                   user=current_user)
            subject = "Please confirm your email"
            send_mail(author.email, subject, html)

            flash('A confirmation email has been sent via email.', 'success')
            # redirects to the unconfirmed route for newly registered users
            return redirect(url_for('auth.unconfirmed'))
    return render_template('auth/register.html', register_form=register_form, user=current_user)


@auth.route('/unconfirmed')
@login_required
def unconfirmed():
    """
    Unconfirmed route for users who have not confirmed their email accounts.
    :return: template for unconfirmed users
    """
    if current_user.confirmed:
        return redirect('dashboard.user_dashboard')
    flash('Please confirm your account!', 'warning')
    return render_template('auth/unconfirmed.html', user=current_user)


@auth.route('/confirm/<token>')
@login_required
def confirm_email(token):
    """
    Confirm email route for the user. Checks if the author has already confirmed their account
    If they have, log them in. If they have not, confirm their account and direct them to their dashboard
    we call the confirm_token() function, passing in the token. If successful, we update the user,
    changing the email_confirmed attribute to True and setting the datetime for when the confirmation took place.
    Also, in case the user already went through the confirmation process – and is confirmed –
    then we alert the user of this.

    :param token: Generated in the user registration
    :return: A redirect to login
    """
    if current_user.confirmed:
        flash('Account already confirmed. Please login.', 'success')
        return redirect(url_for('auth.login'))

    email = confirm_token(token)

    # get the author or throw an error
    author = Author.query.filter_by(email=current_user.email).first_or_404()

    if author.email == email:
        author.confirmed = True
        author.confirmed_on = datetime.now()
        db.session.add(author)
        db.session.commit()
        flash('You have confirmed your account. Thanks!', 'success')
    else:
        flash('The confirmation link is invalid or has expired.', 'danger')

    # redirect to the user's dashboard
    return redirect(url_for('auth.login'))


@auth.route('/forgot-password', methods=["GET", "POST"])
def forgot_password():
    forgot_pass = ForgotPassword(request.form)
    return render_template('auth/password-recovery.html', forgot_pass=forgot_pass, user=current_user)


@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for("home.home"))

